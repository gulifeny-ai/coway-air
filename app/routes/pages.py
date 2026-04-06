from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies import templates, common_context, require_login
from app.services.document_service import get_recent_reports

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    redirect = require_login(request)
    if redirect:
        return redirect
    return RedirectResponse(url="/dashboard")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    redirect = require_login(request)
    if redirect:
        return redirect
    recent = get_recent_reports(5)
    ctx = common_context(request, "대시보드")
    ctx["recent_reports"] = recent
    return templates.TemplateResponse("pages/dashboard.html", ctx)
