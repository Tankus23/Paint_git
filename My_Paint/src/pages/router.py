from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

# from operations.router import get_specific_operations

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/menu")
def get_menu_page(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})

@router.get("/welcome")
def get_menu_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@router.get("/auth")
def get_menu_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register")
def get_menu_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/paint")
def get_paint_page(request: Request):
    return templates.TemplateResponse("paint.html", {"request": request})
