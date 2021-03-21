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
CODE = 'zhern0206eskiy'


def is_t_ok(l1, l2) -> bool:
    # format HH:MM - HH:MM
    time = [0] * 1440
    # print(list(l1) + list(l2))
    for h in list(l1) + list(l2):
        t = h.hours
        b1, b2 = t.split('-')
        a = b1.split(':')
        a = int(a[0]) * 60 + int(a[1])
        b = b2.split(':')
        b = int(b[0]) * 60 + int(b[1])
        time[a] += 1
        time[b + 1] -= 1
        # print(t, b1, b2, a, b, time[a], time[b + 1])
    # print('---------------------------')
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
    already_in_base = [i.id for i in db_sess.query(Courier).all()]
    is_ok = True
    for courier_info in req_json:
        print(set(dict(courier_info).keys()) != courier_fields, courier_info['courier_id'] in already_in_base)
        if set(dict(courier_info).keys()) != courier_fields or courier_info['courier_id'] in already_in_base:
            is_ok = False
            bad_id.append({"id": int(courier_info['courier_id'])})
        if not is_ok:
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

    if is_ok:
        db_sess.commit()
        return jsonify({"couriers": res}), 201
    return jsonify({"validation_error": bad_id}), 400


@blueprint.route('/orders', methods=["POST"])
def add_orders():
    req_json = request.json['data']
    db_sess = db_session.create_session()
    res = []
    bad_id = []
    is_ok = True
    already_in_base = [i.id for i in db_sess.query(Order).all()]
    for order_info in req_json:
        flag = set(dict(order_info).keys()) != order_fields
        if flag or not 0.01 <= order_info['weight'] <= 50 or order_info['order_id'] in already_in_base:
            is_ok = False
            bad_id.append({"id": int(order_info['order_id'])})
        if not is_ok:
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

    if is_ok:
        db_sess.commit()
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
            if k == 'type':
                courier.maxw = c_type[v]
                ords = db_sess.query(Order).filter(Order.orders_courier == courier_id).all()
                for i in sorted(ords, key=lambda p: p.weight, reverse=True):
                    if courier.currentw > courier.maxw:
                        i.orders_courier = 0
                        courier.currentw -= i.weight
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
            if i.complete_time:
                continue
            if i.weight + courier.currentw > courier.maxw or i.region not in res['regions'] or not is_t_ok(dh, a):
                i.orders_courier = 0
                courier.currentw -= i.weight
        db_sess.commit()
        return jsonify(res), 200
    elif request.method == 'GET':
        db_sess = db_session.create_session()
        courier = db_sess.query(Courier).filter(Courier.id == courier_id).first()
        if not courier:
            abort(400)
        res = {}
        res['courier_id'] = courier_id
        res['courier_type'] = rev_c_type[courier.maxw]
        a = [i.hours for i in db_sess.query(WH).filter(WH.courier_id == courier.id).all()]
        res['working_hours'] = a
        b = [i.region for i in db_sess.query(Region).filter(Region.courier_id == courier.id).all()]
        res['regions'] = b
        res['earnings'] = courier.earnings
        if not courier.earnings:
            return jsonify(res), 201
        try:
            t = min([i.summa / i.q
                     for i in db_sess.query(Region).filter(Region.courier_id == courier.id).all()
                     if i.q != 0])
        except ValueError:
            t = 60 * 60
        res['rating'] = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
        return jsonify(res), 201


@blueprint.route('/orders/assign', methods=["POST"])
def assign_orders():
    courier_id = request.json['courier_id']
    db_sess = db_session.create_session()
    courier = db_sess.query(Courier).filter(Courier.id == courier_id).first()
    ords = db_sess.query(Order).filter(Order.orders_courier == courier_id, Order.complete_time == '').all()
    if ords:
        print('didnt all task')
        res = [{'id': i.id} for i in ords]
        return jsonify({'orders': res, 'assign_time': courier.last_assign_time}), 201
    courier_regions = [i.region for i in
                       db_sess.query(Region).filter(Region.courier_id == courier_id).all()]
    courier_wh = db_sess.query(WH).filter(WH.courier_id == courier_id).all()
    if not courier:
        abort(400)

    ords = db_sess.query(Order).filter((Order.orders_courier == 0),  # | (Order.orders_courier == courier_id),
                                       Order.region.in_(courier_regions)).all()
    print(ords)
    for order in sorted(ords, key=lambda x: x.weight):
        if order.weight + courier.currentw > courier.maxw:
            print(order.id, 'go out', courier.currentw)
            break
        if is_t_ok(db_sess.query(DH).filter(DH.order_id == order.id).all(), courier_wh):
            order.orders_courier = courier_id
            courier.currentw += order.weight

    db_sess.commit()

    res = [{'id': order.id} for order in
           db_sess.query(Order).filter(Order.orders_courier == courier_id, '' == Order.complete_time)]
    if not res:
        return jsonify({"orders": []}), 200
    courier.last_pack_cost = kd[courier.maxw] * 500
    courier.last_assign_time = str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    assign_time = str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    if '' == courier.last_delivery_t:
        courier.last_delivery_t = assign_time
    db_sess.commit()
    return jsonify({"orders": res, 'assign_time': str(assign_time)}), 200


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
    reg.q += 1
    u = datetime.datetime.fromisoformat(complete_t.split('.')[0])
    v = datetime.datetime.fromisoformat(courier.last_delivery_t.split('.')[0])
    courier.last_delivery_t = complete_t
    reg.summa += (u - v).total_seconds()
    if order.complete_time == '':
        courier.currentw -= order.weight
    order.complete_time = complete_t
    if not db_sess.query(Order).filter(Order.orders_courier == courier_id, Order.complete_time == '').all():
        courier.earnings += courier.last_pack_cost
        courier.last_pack_cost = 0
    db_sess.commit()
    return jsonify({'order_id': order.id}), 200


@blueprint.route('/test', methods=['GET'])
def test():
    return jsonify({"test": 'connection is here'}), 201


@blueprint.route('/clear', methods=['POST'])
def clear():
    if request.json['code'] != CODE:
        return jsonify({"error": "wrong code"}), 400
    db_sess = db_session.create_session()
    db_sess.query(Courier).delete()
    db_sess.query(Order).delete()
    db_sess.query(Region).delete()
    db_sess.query(WH).delete()
    db_sess.query(DH).delete()
    db_sess.commit()
    return jsonify({'status': 'all data cleared'}), 201