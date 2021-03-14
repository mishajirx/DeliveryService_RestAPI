import flask
from flask import jsonify, abort, request

from data import db_session
from data.couriers import Courier
from data.orders import Order

blueprint = flask.Blueprint(
    'orders_api',
    __name__,
    template_folder='templates'
)