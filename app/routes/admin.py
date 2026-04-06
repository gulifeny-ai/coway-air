from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies import templates, common_context, require_login, get_current_user
from app.services.settings_service import get_settings, update_settings
from app.utils.env_utils import load_env_items

router = APIRouter(prefix="/admin")


@router.get("", response_class=HTMLResponse)
async def admin_page(request: Request):
    redirect = require_login(request)
    if redirect:
        return redirect
    user = get_current_user(request)
    if not user or user["role"] != "admin":
        return RedirectResponse(url="/dashboard", status_code=303)
    settings_list = get_settings()
    ctx = common_context(request, "관리자 설정")
    ctx["settings"] = settings_list
    return templates.TemplateResponse("pages/admin.html", ctx)


@router.post("/settings", response_class=HTMLResponse)
async def save_settings(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "admin":
        return RedirectResponse(url="/dashboard", status_code=303)

    form = await request.form()
    current = load_env_items()
    new_values = {}
    for item in current:
        key = item["key"]
        if key in form:
            new_values[key] = form[key]
        else:
            new_values[key] = item["value"]
    update_settings(new_values)

    # reload config
    from app.config import load_env, settings as app_settings
    app_settings.update(load_env())

    settings_list = get_settings()
    ctx = common_context(request, "관리자 설정")
    ctx["settings"] = settings_list
    ctx["message"] = "설정이 저장되었습니다."
    return templates.TemplateResponse("pages/admin.html", ctx)
