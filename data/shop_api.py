import flask
from flask import jsonify, abort, request, Blueprint

from data import db_session
from data.couriers import Courier
from data.orders import Order
from data.regions import Region
from data.workinghours import WH
from data.deliveryhours import DH
from main import bad_request

blueprint = Blueprint(
    'shop_api',
    __name__,
    template_folder='templates'
)
courier_fields = {'courier_id', 'courier_type', 'regions', 'working_hours'}
order_fields = {'order_id', 'weight', 'region', 'delivery_hours'}
c_type = {'foot': 10, 'bike': 15, 'car': 50}


@blueprint.route('/couriers', methods=["POST"])
def add_couriers():
    req_json = request.json['data']
    db_sess = db_session.create_session()
    res = []
    bad_id = []
    is_ok = True
    for courier_info in req_json:
        print(set(dict(courier_info).keys()))
        if set(dict(courier_info).keys()) != courier_fields:
            is_ok = False
            bad_id.append({"id": int(courier_info['courier_id'])})
            continue
        courier = Courier()
        courier.id = courier_info['courier_id']
        courier.maxw = c_type[courier_info['courier_type']]
        for i in list((courier_info['regions'])):
            reg = Region()
            reg.courier_id = courier.id
            reg.region = i
            db_sess.add(reg)
        for i in list(courier_info['working_hours']):
            wh = WH()
            wh.courier_id = courier.id
            wh.hours = i
            db_sess.add(wh)
        db_sess.add(courier)
        res.append({"id": courier_info['courier_id']})
    db_sess.commit()

    if is_ok:
        return jsonify({"couriers": res}), 201
    return jsonify({"validation_error": bad_id}), 400


@blueprint.route('/orders', methods=["POST"])
def add_orders():
    req_json = request.json['data']
    db_sess = db_session.create_session()
    res = []
    bad_id = []
    is_ok = True
    for order_info in req_json:
        print(set(dict(order_info).keys()))
        if set(dict(order_info).keys()) != order_fields:
            is_ok = False
            bad_id.append({"id": int(order_info['order_id'])})
            continue
        order = Order()
        order.id = order_info['order_id']
        order.weight = order_info['weight']
        order.region = order_info['region']
        order.is_took = False
        for i in list(order_info['delivery_hours']):
            dh = DH()
            dh.order_id = order.id
            dh.hours = i
            db_sess.add(dh)
        db_sess.add(order)
        res.append({"id": int(order_info['order_id'])})
    db_sess.commit()

    if is_ok:
        return jsonify({"orders": res}), 201
    return jsonify({"validation_error": bad_id}), 400


@blueprint.route('/couriers/<courier_id>', methods=["PATCH"])
def edit_courier(courier_id):
    req_json = request.json['data']
    db_sess = db_session.create_session()
    res = []
    is_ok = True
    courier = db_sess.query(Courier).filter(Courier.id == courier_id).first()
    if set(dict(req_json).keys()) != courier_fields:
        for k, v in dict(req_json):
            courier.__setattr__(k, v)
        db_sess.commit()
    if is_ok:
        return jsonify('Информация о клиенте'), 201
    else:
        bad_request(404, 'ahahahha', 'hffhhfhf')


@blueprint.route('/test', methods=['GET'])
def test():
    return jsonify({"a": 2}), 201
