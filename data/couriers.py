import sqlalchemy
from .db_session import SqlAlchemyBase


class Courier(SqlAlchemyBase):
    __tablename__ = 'couriers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    regions = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.INTEGER), nullable=True)
    working_hours = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String), nullable=True)
