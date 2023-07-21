from datetime import datetime
from typing import List

from starlette.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_async_session
from src.pictures.models import picture
from sqlalchemy import select, insert
from fastapi import APIRouter, Request, Depends, Body, HTTPException
from fastapi.templating import Jinja2Templates

from src.pictures.schemas import PicturesCreate
from src.utils.data import get_date, get_current_user_info

router = APIRouter(
    tags=["Picture"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/paint")
def get_paint_page(request: Request):
    return templates.TemplateResponse("paint.html", {"request": request})


@router.get("/paint/", response_class=HTMLResponse)
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
            url=f"/paint/{current_user_info['current_profile_id']}"
        )

    return RedirectResponse(url="/")


@router.post("/paint/{profile_id}")
async def add_specific_pictures(
        image_address: str = Body(),
        current_user_info: User = Depends(get_current_user_info),
        session=Depends(get_async_session)
):
    # Получаем отправителя и получателя по их ID
    id_users = current_user_info['current_profile_id']
    date = datetime.now()
    # Создаем новое сообщение и связываем его с отправителем и получателем

    new_picture = PicturesCreate(
        id_user=id_users,
        date=date,
        image_address=image_address
    )
    stmt = insert(picture).values(**new_picture.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


# @router.post("/paint/{profile_id}")
# async def add_specific_pictures(message: MessageCreate,
#                                 current_user: User = Depends(get_current_user_info),
#                                 session=Depends(get_async_session)):
#     stmt = insert(picture).values(**new_picture.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}


@router.get("/paint/{profile_id}", response_class=HTMLResponse)
def get_profile_by_id(
        request: Request,
        profile_id: int,
        year=Depends(get_date),
        current_user_info=Depends(get_current_user_info),

):
    if not current_user_info["current_username"]:
        # Перенаправляем пользователя на страницу регистрации
        return RedirectResponse(url="/login")

    return templates.TemplateResponse(
        "paint.html",
        {
            "request": request,
            "year": year,
            "user_active": True,
            "current_username": current_user_info["current_username"],
            "profile_id": profile_id,
        },
    )

@router.get("/")
async def get_specific_pictures(profile_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(picture).where(picture.c.id_user == profile_id)
    result = await session.execute(query)

    return {
        'status': 'ok',
        'data': [dict(r._mapping) for r in result]
    }

# @router.put(f"/paint/{profile_id}/{image_address}")
# async def create_picture(username: str, file: UploadFile = File(...)):
#     # Проверяем существование пользователя и выполняем другую логику
#     # ...
#
#     avatar_filename = f"{username}.png"
#     avatar_path = os.path.join(storage_directory, avatar_filename)
#
#     # Удаляем старую аватарку, если она существует
#     if os.path.exists(avatar_path):
#         os.remove(avatar_path)
#
#     # Сохраняем новую аватарку
#     with open(avatar_path, "wb") as f:
#         f.write(await file.read())
#
#     return {"message": "Avatar updated successfully"}
# @router.get("/")
# async def get_specific_picture(picture_date: datetime, session: AsyncSession = Depends(get_async_session)):
#     query = select(picture).where(picture.c.date == picture_date)
#     result = await session.execute(query)
#     return result.all()
#
#
# @router.post("/")
# async def add_specific_picture(new_picture: PicturesCreate, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(picture).values(**new_picture.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}
