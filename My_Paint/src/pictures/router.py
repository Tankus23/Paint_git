from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.pictures.models import picture
from src.pictures.schemas import PicturesCreate

router = APIRouter(
    prefix="/pictures",
    tags=["Picture"]
)


@router.get("/")
async def get_specific_picture(picture_date: datetime, session: AsyncSession = Depends(get_async_session)):
    query = select(picture).where(picture.c.date == picture_date)
    result = await session.execute(query)
    return result.all()


@router.post("/")
async def add_specific_picture(new_picture: PicturesCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(picture).values(**new_picture.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
