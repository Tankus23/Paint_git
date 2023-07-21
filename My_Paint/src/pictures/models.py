from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey

from src.auth.models import user

metadata = MetaData()

picture = Table(
    "picture",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_user", Integer, ForeignKey(user.c.id)),
    Column("date", TIMESTAMP),
    Column("image_address", String),
)
