import sqlalchemy
from data.db_session import SqlAlchemyBase


class Courier(SqlAlchemyBase):
    __tablename__ = 'couriers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    maxw = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    amount_deliveries = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    last_delivery_t = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')
