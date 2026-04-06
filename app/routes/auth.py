from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies import templates
from app.services.auth_service import authenticate
from app.config import APP_TITLE

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("pages/login.html", {
        "request": request,
        "app_title": APP_TITLE,
        "error": None,
    })


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form("")):
    user = authenticate(username, password)
    if not user:
        return templates.TemplateResponse("pages/login.html", {
            "request": request,
            "app_title": APP_TITLE,
            "error": "아이디 또는 비밀번호가 올바르지 않습니다.",
        })
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="username", value=user["username"], httponly=True)
    response.set_cookie(key="role", value=user["role"], httponly=True)
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("username")
    response.delete_cookie("role")
    return response
