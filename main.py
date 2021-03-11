from flask import Flask, make_response, jsonify, abort, request
from data import db_session
from data.couriers import Courier
from data.orders import Order

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
fields = {'courier_id', 'courier_type', 'regions', 'working_hours'}
c_type = {'foot': 10, 'bike': 15, 'car': 50}
x = 0


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def hello():
    return 'Hello go+ Misha'


@app.route('/couriers', methods=["POST"])
def add_couriers():
    # global x
    # x = request.json['x']
    # return 'ok', 201
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


@app.route('/couriers/<courier_id>', methods=["PATCH"])
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


@app.route('/g', methods=['GET'])
def get_couriers():
    return str(x), 201


def main():
    db_session.global_init("db/couriers.db")
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
