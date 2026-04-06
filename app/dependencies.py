from typing import Optional
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.config import BASE_DIR, APP_TITLE

templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


def get_current_user(request: Request) -> Optional[dict]:
    username = request.cookies.get("username")
    role = request.cookies.get("role")
    if not username:
        return None
    return {"username": username, "role": role or "guest"}


def require_login(request: Request) -> Optional[RedirectResponse]:
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return None


def common_context(request: Request, page_title: str = "") -> dict:
    user = get_current_user(request)
    return {
        "request": request,
        "app_title": APP_TITLE,
        "page_title": page_title,
        "user": user,
    }
