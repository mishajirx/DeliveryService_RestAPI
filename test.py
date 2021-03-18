import datetime
import requests


def add_couriers(*args):
    data = {'data': []}
    for i in args:
        x = {}
        x['courier_id'], x['courier_type'], x['regions'], x['working_hours'] = i
        data['data'].append(x)
    url = 'http://127.0.0.1:5000/couriers'
    print(requests.post(url, json=data).json())


def add_orders(*args):
    data = {'data': []}
    for i in args:
        x = {}
        x['order_id'], x['weight'], x['region'], x['delivery_hours'] = i
        data['data'].append(x)
    url = 'http://127.0.0.1:5000/orders'
    print(requests.post(url, json=data).json())


def edit_courier(c, *args):
    url = 'http://127.0.0.1:5000/couriers/' + c
    data = {}
    for k, v in args:
        data[k] = v
    print(requests.patch(url, json=data).json())


def get_courier(c):
    url = 'http://127.0.0.1:5000/couriers/' + c
    print(requests.get(url).json())


def assign_orders(c_id):
    url = 'http://127.0.0.1:5000/orders/assign'
    data = {
        'courier_id': c_id
    }
    print(requests.post(url, json=data).json())


def complete_orders(c_id, o_id, complete_t):
    url = 'http://127.0.0.1:5000/orders/complete'
    data = {
        'courier_id': c_id,
        'order_id': o_id,
        'complete_time': complete_t
    }
    print(requests.post(url, json=data).json())


test_url = 'http://127.0.0.1:5000/test'
print(requests.get(test_url).json())
