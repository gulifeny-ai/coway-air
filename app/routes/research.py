from typing import Optional
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from app.dependencies import templates, common_context, require_login, get_current_user
from app.services.research_service import (
    get_research_list,
    get_research,
    create_research,
    collect_company_data,
    collect_web_data,
    get_stats,
)
from app.clients.dart_client import get_company_detail_by_code, get_financial_statements
from app.clients.google_search_client import search_web
from app.clients.news_client import search_news_direct
from app.services.dart_corp_service import search_corps, get_corp_by_code, get_total_count
from app.clients.openai_client import chat_completion

router = APIRouter(prefix="/research")


@router.get("", response_class=HTMLResponse)
async def research_page(request: Request):
    redirect = require_login(request)
    if redirect:
        return redirect
    stats = get_stats()
    researches = get_research_list()
    ctx = common_context(request, "시장조사")
    ctx["stats"] = stats
    ctx["researches"] = researches
    return templates.TemplateResponse("pages/research.html", ctx)


@router.get("/search", response_class=HTMLResponse)
async def search_researches(request: Request, q: str = ""):
    researches = get_research_list(q)
    return templates.TemplateResponse(
        "partials/research_list.html",
        {"request": request, "researches": researches, "query": q},
    )


@router.get("/new", response_class=HTMLResponse)
async def new_research_page(request: Request):
    redirect = require_login(request)
    if redirect:
        return redirect
    ctx = common_context(request, "새 리서치")
    return templates.TemplateResponse("pages/research_new.html", ctx)


@router.get("/dart-search", response_class=HTMLResponse)
async def dart_search(request: Request, q: str = ""):
    results = search_corps(q, limit=10)
    return templates.TemplateResponse(
        "partials/dart_search_result.html",
        {"request": request, "results": results, "query": q, "total": get_total_count()},
    )


@router.post("/lookup-companies", response_class=HTMLResponse)
async def lookup_companies(request: Request, companies: str = Form("")):
    """companies = "기업명|코드,기업명|코드,..." 형태 → corp_code로 DART API 조회"""
    results = []
    errors = []
    for item in companies.split(","):
        item = item.strip()
        if not item:
            continue
        parts = item.split("|")
        name = parts[0]
        code = parts[1] if len(parts) > 1 else ""
        if code:
            detail = await get_company_detail_by_code(code)
            if detail:
                results.append(detail)
            else:
                errors.append(name)
        else:
            errors.append(name)
    return templates.TemplateResponse(
        "partials/company_lookup_results.html",
        {"request": request, "companies": results, "errors": errors},
    )


@router.post("/lookup-companies-json")
async def lookup_companies_json(request: Request, companies: str = Form("")):
    """기업 상세 정보 + 재무제표를 JSON으로 반환 (AI 리서치용)"""
    results = []
    for item in companies.split(","):
        item = item.strip()
        if not item:
            continue
        parts = item.split("|")
        code = parts[1] if len(parts) > 1 else ""
        if code:
            detail = await get_company_detail_by_code(code)
            if detail:
                entry = detail.dict()
                fin = await get_financial_statements(code)
                entry["financial"] = {}
                for report_key, items in fin.items():
                    entry["financial"][report_key] = [
                        {"account_nm": r["account_nm"], "sj_nm": r["sj_nm"],
                         "thstrm_amount": r.get("thstrm_amount", ""),
                         "frmtrm_amount": r.get("frmtrm_amount", ""),
                         "bfefrmtrm_amount": r.get("bfefrmtrm_amount", "")}
                        for r in items
                    ]
                results.append(entry)
    return results


@router.post("/lookup-financial", response_class=HTMLResponse)
async def lookup_financial(request: Request, corp_code: str = Form(...), corp_name: str = Form("")):
    """선택된 기업의 전체 재무제표 조회 (올해+작년, 4개 보고서)"""
    data = await get_financial_statements(corp_code)
    return templates.TemplateResponse(
        "partials/financial_results.html",
        {"request": request, "financial_data": data, "corp_name": corp_name, "corp_code": corp_code},
    )


@router.post("/search-web", response_class=HTMLResponse)
async def search_web_keywords(request: Request, company_name: str = Form(""), keywords: str = Form("")):
    query = f"{company_name} {keywords}".strip()
    results = await search_web(query) if query else []
    return templates.TemplateResponse(
        "partials/web_search_result.html",
        {"request": request, "results": results, "query": query},
    )


@router.post("/search-news", response_class=HTMLResponse)
async def search_news_keywords(request: Request, company_name: str = Form(""), keywords: str = Form("")):
    """키워드 기반 뉴스 검색 (직전 1주일, 인기도순)"""
    # company_name + keywords를 합쳐서 하나의 검색어로
    parts = []
    if company_name.strip():
        parts.append(company_name.strip())
    for k in keywords.split(","):
        k = k.strip()
        if k:
            parts.append(k)
    query = " ".join(parts)
    print(f"[search-news] company_name='{company_name}', keywords='{keywords}' -> query='{query}'")
    if not query:
        return templates.TemplateResponse(
            "partials/news_results.html",
            {"request": request, "news": {"articles": []}, "error": "키워드를 입력하세요."},
        )
    news = await search_news_direct(query)
    return templates.TemplateResponse(
        "partials/news_results.html",
        {"request": request, "news": news},
    )


DEFAULT_SYSTEM_PROMPT = (
    "당신은 코웨이 주식회사의 Coway-AIR 시스템의 시니어 리서치 분석가입니다.\n\n"
    "## 역할 및 규칙\n"
    "- 제공된 기업 정보(DART 전자공시)와 뉴스 데이터를 기반으로 전문적인 조사 보고서를 작성합니다.\n"
    "  - 제공되는 기업들의 정보는 한개 이상입니다. 한개 이상이면 기업들의 정보를 비교해서 조사를 해야합니다.\n"
    "- 제공되는 뉴스 기사들은 인터넷의 동향정보입니다. 해당 정보들을 기반으로 최대한 주제에 맞게 전략적인 사고를 해야합니다.\n"
    "- 데이터에 없는 내용은 추측하지 않고, 데이터 기반으로만 분석합니다.\n\n"
    "## 보고서 형식 (마크다운)\n"
    "1. **핵심 요약** (Executive Summary) - 3~5줄로 핵심 내용 요약\n"
    "2. **기업 개요** - 제공된 기업 정보 기반 정리\n"
    "3. **최신 동향 분석** - 뉴스 데이터 기반 주요 이슈 분석\n"
    "4. **시장 환경 및 경쟁 분석** - 업종, 경쟁 구도 분석\n"
    "5. **리스크 요인** - 잠재적 위험 요소\n"
    "6. **시사점 및 제언** - 종합적 판단과 제안\n\n"
    "## 작성 규칙\n"
    "- 한국어로 작성\n"
    "- 마크다운 형식 (제목, 리스트, 볼드, 테이블 활용)\n"
    "- 객관적이고 전문적인 어조\n"
    "- 뉴스 인용 시 출처 명시\n"
)


@router.get("/default-prompt")
async def get_default_prompt():
    return {"system_prompt": DEFAULT_SYSTEM_PROMPT}


@router.post("/ai-research", response_class=HTMLResponse)
async def ai_research(
    request: Request,
    prompt: str = Form(""),
    system_prompt: str = Form(""),
    company_data: str = Form(""),
    news_data: str = Form(""),
):
    """수집된 기업정보 + 선택된 뉴스를 컨텍스트로 OpenAI에 리서치 요청"""
    print(f"[ai-research] prompt='{prompt[:100]}'")
    print(f"[ai-research] system_prompt length={len(system_prompt)}")
    print(f"[ai-research] company_data length={len(company_data)}")
    print(f"[ai-research] news_data length={len(news_data)}")

    # 시스템 프롬프트: 사용자 커스텀 or 기본값
    sys_prompt = system_prompt.strip() if system_prompt.strip() else DEFAULT_SYSTEM_PROMPT

    # 컨텍스트 구성
    context_parts = []
    if company_data.strip():
        context_parts.append(
            "## 기업 정보 (DART 전자공시 기반)\n"
            "아래는 대상 기업의 공식 등록 정보입니다.\n\n"
            + company_data
        )
    if news_data.strip():
        context_parts.append(
            "## 관련 뉴스 기사\n"
            "아래는 사용자가 선택한 관련 뉴스입니다.\n\n"
            + news_data
        )
    context = "\n\n---\n\n".join(context_parts)

    user_prompt = f"## 리서치 요청 내용\n{prompt}\n\n"
    if context:
        user_prompt += f"## 참고 데이터\n\n{context}\n\n"
    user_prompt += "위 데이터를 기반으로 조사 보고서를 마크다운 형식으로 작성해주세요."

    result = await chat_completion(sys_prompt, user_prompt)

    return templates.TemplateResponse(
        "partials/ai_research_result.html",
        {
            "request": request,
            "prompt": prompt,
            "result": result,
            "company_data": company_data,
            "news_data": news_data,
        },
    )


@router.post("/create", response_class=HTMLResponse)
async def create(
    request: Request,
    title: str = Form(...),
    topic: str = Form(...),
    company_name: str = Form(""),
    keywords: str = Form(""),
    ai_report: str = Form(""),
):
    from app.utils.file_store import save_markdown
    from app.config import REPORTS_DIR
    from datetime import datetime

    user = get_current_user(request)
    creator = user["username"] if user else "unknown"
    research = create_research(title, topic, company_name, keywords, creator)

    # AI 보고서가 있으면 마크다운으로 저장
    saved_filename = ""
    if ai_report.strip():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = title.replace(" ", "_").replace("/", "_")[:50]
        filename = f"{safe_title}_{timestamp}.md"
        save_markdown(REPORTS_DIR, filename, ai_report)
        saved_filename = filename
        print(f"[create] 보고서 저장: {filename}")

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/reports", status_code=303)


@router.get("/{research_id}", response_class=HTMLResponse)
async def research_detail(request: Request, research_id: str):
    redirect = require_login(request)
    if redirect:
        return redirect
    research = get_research(research_id)
    if not research:
        ctx = common_context(request, "시장조사")
        ctx["error"] = "리서치를 찾을 수 없습니다."
        return templates.TemplateResponse("pages/research.html", ctx)
    ctx = common_context(request, research.title)
    ctx["research"] = research
    ctx["step"] = research.status
    return templates.TemplateResponse("pages/research_detail.html", ctx)


@router.post("/{research_id}/collect-company", response_class=HTMLResponse)
async def step_collect_company(request: Request, research_id: str):
    research = await collect_company_data(research_id)
    return templates.TemplateResponse(
        "partials/research_company_data.html",
        {"request": request, "research": research},
    )


@router.post("/{research_id}/collect-web", response_class=HTMLResponse)
async def step_collect_web(request: Request, research_id: str):
    research = await collect_web_data(research_id)
    return templates.TemplateResponse(
        "partials/research_web_data.html",
        {"request": request, "research": research},
    )
