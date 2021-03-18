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
    url = 'http://127.0.0.1:5000/couriers/' + str(c)
    data = {}
    for k, v in args:
        data[k] = v
    print(requests.patch(url, json=data).json())


def get_courier(c):
    url = 'http://127.0.0.1:5000/couriers/' + str(c)
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

# add_couriers([1, 'foot', [1, 12, 22], ['11:00-13:00', '18:00-22:00']]) passed
# edit_courier(1, ('regions', [13, 55]))
# add_orders([9, 0.4, 13, ['12:00-12:30']])
# assign_orders(1) passed
# add_orders([10, 0.4, 13, ['12:00-12:30']], [11, 40, 13, ['12:00-12:30']]) passed
# edit_courier(1, ('regions', [20, 40])) passed
# assign_orders(1) passed
# edit_courier(1, ('regions', [13, 20])) passed
# assign_orders(1) passed
# edit_courier(1, ('working_hours', [])) passed
# edit_courier(1, ('working_hours', ['11:00-13:00', '18:00-22:00'])) passed
# assign_orders(1) passed
# complete_orders(1, 1, '2021-01-10T10:33:01.42Z') not passed
# add_orders([2, 0.5, 20, ['11:00-13:30']]) passed
# assign_orders(1) passed
# complete_orders(1, 2, '2021-04-10T10:33:01.42Z') passed
# did commit
# add_orders([3, 0.5, 13, ['11:00-13:30']]) passed
# assign_orders(1) passed
# complete_orders(1, 3, '2021-04-10T10:53:01.42Z') passed
# did comit
# add_couriers([1, 'foot', [1, 12, 22], ['11:00-13:00', '18:00-22:00']])
# edit_courier(1, ('regions', [13, 55]))
# add_orders([9, 0.4, 13, ['12:00-12:30']])
# assign_orders(1)
# add_orders([10, 0.4, 13, ['12:00-12:30']], [11, 40, 13, ['12:00-12:30']])
# assign_orders(1) passed
# complete_orders(1, 9, '2021-03-18T18:22:12.680455Z') passed
# assign_orders(1) passed
# add_orders([12, 5, 13, ['12:00-12:30']], [13, 6, 13, ['12:00-12:30']]) passed
# complete_orders(1, 10, '2021-03-18T21:24:23.680455Z') passed
# assign_orders(1) passed
# assign_orders(1) passed
complete_orders(1, 12, '2021-03-18T21:36:00.680455Z')
