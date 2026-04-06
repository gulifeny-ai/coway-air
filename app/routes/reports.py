from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.dependencies import templates, common_context, require_login
from app.services.document_service import get_recent_reports, get_report_content

router = APIRouter(prefix="/reports")


@router.get("", response_class=HTMLResponse)
async def reports_page(request: Request):
    redirect = require_login(request)
    if redirect:
        return redirect
    reports = get_recent_reports(50)
    ctx = common_context(request, "보고서")
    ctx["reports"] = reports
    return templates.TemplateResponse("pages/reports.html", ctx)


@router.get("/{filename}", response_class=HTMLResponse)
async def report_view(request: Request, filename: str):
    redirect = require_login(request)
    if redirect:
        return redirect
    content = get_report_content(filename)
    if not content:
        ctx = common_context(request, "보고서")
        ctx["reports"] = get_recent_reports(50)
        ctx["error"] = "보고서를 찾을 수 없습니다."
        return templates.TemplateResponse("pages/reports.html", ctx)
    ctx = common_context(request, filename.replace("_", " ").replace(".md", ""))
    ctx["filename"] = filename
    ctx["content"] = content
    return templates.TemplateResponse("pages/report_view.html", ctx)
