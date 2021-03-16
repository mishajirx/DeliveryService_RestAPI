import flask
from flask import jsonify, abort, request, Blueprint

from data import db_session
from data.couriers import Courier
from data.orders import Order
from data.regions import Region
from data.workinghours import WH
from data.deliveryhours import DH

blueprint = Blueprint(
    'shop_api',
    __name__,
    template_folder='templates'
)
fields = {'courier_id', 'courier_type', 'regions', 'working_hours'}
c_type = {'foot': 10, 'bike': 15, 'car': 50}


@blueprint.route('/couriers', methods=["POST"])
def add_couriers():
    req_json = request.json['data']
    db_sess = db_session.create_session()
    res = []
    bad_id = []
    is_ok = True
    for courier_info in req_json:
        if set(dict(courier_info).keys()) != fields:
            is_ok = False
            bad_id.append(int(courier_info['courier_id']))
            continue
        courier = Courier()
        courier.id = int(courier_info['courier_id'])
        courier.maxw = c_type[str(courier_info['courier_type'])]
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
        res.append({"id": int(courier_info['courier_id'])})
    db_sess.commit()

    if is_ok:
        return jsonify({"couriers": res}), 201
    abort(400)


@blueprint.route('/couriers/<courier_id>', methods=["PATCH"])
def edit_courier(courier_id):
    req_json = request.json['data']
    db_sess = db_session.create_session()
    res = []
    is_ok = True
    courier = db_sess.query(Courier).filter(Courier.id == courier_id).first()
    if set(dict(req_json).keys()) != fields:
        for k, v in dict(req_json):
            courier.__setattr__(k, v)
        db_sess.commit()
    if is_ok:
        return jsonify('Информация о клиенте'), 201
    else:
        abort(400)


@blueprint.route('/test', methods=['GET'])
def test():
    return jsonify({"a": 2}), 201
