from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey

metadata = MetaData()

operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_user", Integer, ForeignKey('user.id', ondelete='CASCADE'),),
    Column("date", TIMESTAMP),
    Column("image", String),
)