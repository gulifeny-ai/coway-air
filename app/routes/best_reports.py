from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from app.dependencies import templates, common_context, require_login
from app.services.best_report_service import (
    get_best_reports,
    upload_best_report,
    remove_best_report,
)

router = APIRouter(prefix="/best-reports")


@router.get("", response_class=HTMLResponse)
async def best_reports_page(request: Request):
    redirect = require_login(request)
    if redirect:
        return redirect
    reports = get_best_reports()
    ctx = common_context(request, "우수 보고서")
    ctx["reports"] = reports
    return templates.TemplateResponse("pages/best_reports.html", ctx)


@router.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    upload_best_report(file.filename or "uploaded.md", content)
    reports = get_best_reports()
    return templates.TemplateResponse(
        "partials/best_report_list.html",
        {"request": request, "reports": reports},
    )


@router.post("/delete", response_class=HTMLResponse)
async def delete(request: Request, filename: str = Form(...)):
    remove_best_report(filename)
    reports = get_best_reports()
    return templates.TemplateResponse(
        "partials/best_report_list.html",
        {"request": request, "reports": reports},
    )
