from datetime import datetime

from pydantic import BaseModel


class PicturesCreate(BaseModel):
    id: int
    id_user: int
    date: datetime
    image_address: str
