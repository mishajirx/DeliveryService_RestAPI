from flask import Flask, make_response, jsonify, abort, request, blueprints
from data import db_session, shop_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
x = 0


@app.errorhandler(400)
def bad_request(error, *args):
    return make_response(jsonify({'error': 'Bad Request'}), 400)
#
#
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def hello():
    return 'Hello go+ Misha'


def main():
    db_session.global_init("db/couriers.db")
    app.register_blueprint(shop_api.blueprint)
    #app.run()
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
