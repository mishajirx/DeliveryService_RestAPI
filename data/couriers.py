import sqlalchemy
from YandexBackend.data.db_session import SqlAlchemyBase


class Courier(SqlAlchemyBase):
    __tablename__ = 'couriers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    maxw = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
