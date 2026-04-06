import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from app.config import RESEARCH_DIR
from app.models.schemas import Research, ResearchStats, CompanyDetail, WebSearchResult
from app.clients.dart_client import get_company_detail_by_code
from app.clients.google_search_client import search_web
from app.services.dart_corp_service import search_corps


def _load_all() -> List[Research]:
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for f in sorted(RESEARCH_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        data = json.loads(f.read_text(encoding="utf-8"))
        items.append(Research(**data))
    return items


def _save(research: Research) -> None:
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    path = RESEARCH_DIR / f"{research.id}.json"
    data = json.loads(research.json())
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def get_research_list(query: str = "") -> List[Research]:
    items = _load_all()
    if query:
        q = query.lower()
        items = [
            r for r in items
            if q in r.title.lower()
            or q in r.topic.lower()
            or q in r.company_name.lower()
            or any(q in kw.lower() for kw in r.keywords)
        ]
    return items


def get_research(research_id: str) -> Optional[Research]:
    path = RESEARCH_DIR / f"{research_id}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return Research(**data)


def create_research(title: str, topic: str, company_name: str, keywords_str: str, creator: str) -> Research:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
    research = Research(
        id=uuid.uuid4().hex[:12],
        title=title,
        topic=topic,
        company_name=company_name,
        keywords=keywords,
        status="draft",
        creator=creator,
        created_at=now,
        updated_at=now,
    )
    _save(research)
    return research


async def collect_company_data(research_id: str) -> Optional[Research]:
    research = get_research(research_id)
    if not research:
        return None
    # corp_code로 DART API 조회
    corps = search_corps(research.company_name, limit=1)
    if corps:
        detail = await get_company_detail_by_code(corps[0]["corp_code"])
        research.company_data = detail
    research.status = "collecting"
    research.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    _save(research)
    return research


async def collect_web_data(research_id: str) -> Optional[Research]:
    research = get_research(research_id)
    if not research:
        return None
    query = f"{research.company_name} {research.topic} {' '.join(research.keywords)}"
    results = await search_web(query)
    research.web_results = [WebSearchResult(**r) for r in results]
    research.status = "analyzing"
    research.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    _save(research)
    return research


def get_stats() -> ResearchStats:
    items = _load_all()
    now = datetime.now()
    this_week = sum(
        1 for r in items
        if (now - datetime.strptime(r.created_at, "%Y-%m-%d %H:%M")).days < 7
    )
    companies = len(set(r.company_name for r in items if r.company_name))
    return ResearchStats(
        total=len(items),
        in_progress=sum(1 for r in items if r.status in ("draft", "collecting", "analyzing")),
        completed=sum(1 for r in items if r.status == "completed"),
        companies_count=companies,
        this_week=this_week,
    )
