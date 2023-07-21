from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

# from operations.router import get_specific_operations

router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")

@router.get("/menu")
def get_menu_page(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})

@router.get("/welcome")
def get_menu_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@router.get("/paint")
def get_paint_page(request: Request):
    return templates.TemplateResponse("paint.html", {"request": request})
