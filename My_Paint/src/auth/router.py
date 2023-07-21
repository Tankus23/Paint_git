import fastapi
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette import status
from src.pictures.router import get_specific_pictures
from .manager import get_user_manager
from .models import User
from .base_config import auth_backend, fastapi_users, current_user
from .schemas import UserCreate, UserRead
from ..utils.data import get_date, get_current_user_info, get_user_info

router = APIRouter(
    tags=["Auth"],
)
templates = Jinja2Templates(directory="src/templates")


@router.get("/register", response_class=HTMLResponse)
def register(request: Request, year=Depends(get_date), user_info=Depends(get_current_user_info)):
    return templates.TemplateResponse("register.html", {
        "request": request,
        "year": year,
        "user_active": user_info["user_active"],
        "current_username": user_info["current_username"]})


@router.get("/login", response_class=HTMLResponse)
def login(request: Request, year=Depends(get_date), user_info=Depends(get_current_user_info)):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "year": year,
        "user_active": user_info["user_active"],
        "current_username": user_info["current_username"]})


@router.get("/profile/", response_class=HTMLResponse)
def get_profile(
        request: Request,
        year=Depends(get_date),
        current_user_info=Depends(get_current_user_info),
):
    if not current_user_info["current_username"]:
        # Перенаправляем пользователя на страницу регистрации
        return RedirectResponse(url="/login")

    if current_user_info["current_profile_id"] is not None:
        return RedirectResponse(
            url=f"/profile/{current_user_info['current_profile_id']}"
        )

    return RedirectResponse(url="/")

# @router.get("/search/{operation_type}")
# def get_search_page(request: Request, operations=Depends(get_specific_operations)):
#     return templates.TemplateResponse("search.html", {"request": request, "operations": operations["data"]})


@router.get("/profile/{profile_id}", response_class=HTMLResponse)
def get_profile_by_id(
        request: Request,
        profile_id: int,
        pictures=Depends(get_specific_pictures),
        current_user_info=Depends(get_current_user_info),

):
    if not current_user_info["current_username"]:
        # Перенаправляем пользователя на страницу регистрации
        return RedirectResponse(url="/login")

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "picture": pictures,
            "user_active": True,
            "current_username": current_user_info["current_username"],
            "profile_id": profile_id,
        },
    )


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/delete-user")
async def delete_user(
        user: User = Depends(fastapi_users.current_user(active=True)),
        user_manager=Depends(get_user_manager),
):
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    # Удаление пользователя из базы данных
    await user_manager.delete(user)
    return fastapi.responses.RedirectResponse(
        '/welcome',
        status_code=status.HTTP_302_FOUND)
