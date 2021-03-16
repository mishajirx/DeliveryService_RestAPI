import flask
from flask import jsonify, abort, request

from data import db_session
from data.couriers import Courier
from data.orders import Order

blueprint = flask.Blueprint(
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
    is_ok = True
    for courier_info in req_json:
        if set(dict(courier_info).keys()) != fields:
            is_ok = False
        courier = Courier()
        res.append({"id": int(courier_info['courier_id'])})
        courier.id = int(courier_info['courier_id'])
        courier.maxw = c_type[str(courier_info['courier_type'])]
        courier.regions = list((courier_info['regions']))
        courier.working_hours = list(courier_info['working_hours'])
        db_sess.add(courier)
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


@blueprint.route('/g', methods=['GET'])
def get_couriers():
    return 'okay'
