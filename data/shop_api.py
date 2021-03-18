import datetime

import flask
from flask import jsonify, abort, request, Blueprint
from sqlite3 import connect

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
courier_fields = {'courier_id', 'courier_type', 'regions', 'working_hours'}
order_fields = {'order_id', 'weight', 'region', 'delivery_hours'}
c_type = {'foot': 10, 'bike': 15, 'car': 50}
rev_c_type = {10: 'foot', 15: 'bike', 50: 'car'}
kd = {10: 2, 15: 5, 50: 9}


def is_t_ok(l1, l2) -> bool:
    # format HH:MM - HH:MM
    time = [0] * 1440
    for h in list(l1) + list(l2):
        t = h.hours
        # print(t)
        b1, b2 = t.split('-')
        a = b1.split(':')
        a = int(a[0]) * 60 + int(a[1])
        b = b2.split(':')
        b = int(b[0]) * 60 + int(b[1])
        time[a] += 1
        time[b + 1] -= 1
    balance = 0
    for i in time:
        balance += i
        if balance >= 2:
            return True
    return False


@blueprint.route('/couriers', methods=["POST"])
def add_couriers():
    req_json = request.json['data']
    db_sess = db_session.create_session()
    res = []
    bad_id = []
    is_ok = True
    for courier_info in req_json:
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
        if set(dict(order_info).keys()) != order_fields:
            is_ok = False
            bad_id.append({"id": int(order_info['order_id'])})
            continue
        order = Order()
        order.id = order_info['order_id']
        order.weight = order_info['weight']
        order.region = order_info['region']
        order.orders_courier = 0
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


@blueprint.route('/couriers/<courier_id>', methods=["PATCH", "GET"])
def edit_courier(courier_id):
    if request.method == 'PATCH':
        req_json = request.json
        db_sess = db_session.create_session()
        courier = db_sess.query(Courier).filter(Courier.id == courier_id).first()
        if not (set(req_json.keys()) <= courier_fields):
            abort(400)
        for k, v in dict(req_json).items():
            if k == 'id':
                courier.id = v
            elif k == 'type':
                courier.maxw = c_type[v]
            elif k == 'regions':
                db_sess.query(Region).filter(Region.courier_id == courier.id).delete()
                for i in v:
                    reg = Region()
                    reg.courier_id = courier.id
                    reg.region = i
                    db_sess.add(reg)
            elif k == 'working_hours':
                db_sess.query(WH).filter(WH.courier_id == courier.id).delete()
                for i in v:
                    wh = WH()
                    wh.courier_id = courier.id
                    wh.hours = i
                    db_sess.add(wh)
        db_sess.commit()
        res = {}
        res['courier_id'] = courier_id
        res['courier_type'] = rev_c_type[courier.maxw]
        a = db_sess.query(WH).filter(WH.courier_id == courier.id).all()
        res['working_hours'] = [i.hours for i in a]
        b = [i.region for i in db_sess.query(Region).filter(Region.courier_id == courier.id).all()]
        res['regions'] = b
        for i in db_sess.query(Order).filter(Order.orders_courier == courier_id).all():
            dh = db_sess.query(DH).filter(DH.order_id == i.id).all()
            print('hghghghghg', i.region)
            if i.weight > courier.maxw or i.region not in res['regions'] or not is_t_ok(dh, a):
                i.orders_courier = 0
        db_sess.commit()
        return jsonify(res), 201
    elif request.method == 'GET':
        db_sess = db_session.create_session()
        courier = db_sess.query(Courier).filter(Courier.id == courier_id).first()
        res = {}
        res['courier_id'] = courier_id
        res['courier_type'] = rev_c_type[courier.maxw]
        a = [i.hours for i in db_sess.query(WH).filter(WH.courier_id == courier.id).all()]
        res['working_hours'] = a
        b = [i.region for i in db_sess.query(Region).filter(Region.courier_id == courier.id).all()]
        res['regions'] = b
        res['earnings'] = courier.amount_deliveries * 500 * kd[courier.maxw]
        t = min([i.summa / i.q
                 for i in db_sess.query(Region).filter(Region.courier_id == courier.id).all()
                 if i.q != 0])
        print((60 * 60 - min(t, 60 * 60)), (60 * 60) * 5)
        res['rating'] = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
        return jsonify(res), 201


@blueprint.route('/orders/assign', methods=["POST"])
def assign_orders():
    courier_id = request.json['courier_id']
    db_sess = db_session.create_session()
    courier = db_sess.query(Courier).filter(Courier.id == courier_id).first()
    if not courier:
        abort(400)
    ords = db_sess.query(Order).filter(
        # график работы совпадает с графиком доставки
        is_t_ok(db_sess.query(WH).filter(WH.courier_id == courier_id).all(),
                db_sess.query(DH).filter(DH.order_id == Order.id).all()),
        # регион подходит
        Order.region.in_(
            [i.region for i in db_sess.query(Region).filter(Region.courier_id == courier_id).all()]
        ),
        (Order.orders_courier == 0) | (Order.orders_courier == courier_id)
    ).all()
    for order in ords:
        order.orders_courier = courier_id
    print(ords)
    db_sess.commit()
    res = [{'id': order.id} for order in
           db_sess.query(Order).filter(
               Order.orders_courier == courier_id, '' == Order.complete_time
           )
           ]
    if not res:
        return jsonify({"orders": res}), 201
    assign_time = str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    if '' == courier.last_delivery_t:
        courier.last_delivery_t = assign_time
    courier.amount_deliveries += 1
    db_sess.commit()
    return jsonify({"orders": res, 'assign_time': str(assign_time)}), 201


@blueprint.route('/orders/complete', methods=["POST"])
def complete_orders():
    req_json = request.json
    db_sess = db_session.create_session()
    courier_id = req_json['courier_id']
    order_id = req_json['order_id']
    complete_t = req_json['complete_time']
    courier = db_sess.query(Courier).filter(Courier.id == courier_id).first()
    order = db_sess.query(Order).filter(Order.id == order_id).first()
    if not courier or not order or order.orders_courier != courier.id:
        abort(400)
    db_sess.commit()
    reg = db_sess.query(Region).filter(
        Region.region == order.region, Region.courier_id == courier_id
    ).first()
    courier.last_delivery_t = complete_t
    reg.q += 1
    u = datetime.datetime.fromisoformat(complete_t.split('.')[0])
    v = datetime.datetime.fromisoformat(courier.last_delivery_t.split('.')[0])
    reg.summa += (u - v).total_seconds()
    order.complete_time = complete_t
    db_sess.commit()
    return jsonify({'order_id': order.id}), 201


@blueprint.route('/test', methods=['GET'])
def test():
    return jsonify({"a": 2}), 201
