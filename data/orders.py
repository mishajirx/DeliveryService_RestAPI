import sqlalchemy
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    region = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)