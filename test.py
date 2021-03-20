import datetime
import requests

HOST = '127.0.0.1'


def add_couriers(*args):
    data = {'data': []}
    for i in args:
        x = {}
        x['courier_id'], x['courier_type'], x['regions'], x['working_hours'] = i
        data['data'].append(x)
    url = f'http://{HOST}:8080/couriers'
    response = requests.post(url, json=data)
    if not response:
        print(response)
    print(response, response.json())


def add_orders(*args):
    data = {'data': []}
    for i in args:
        x = {}
        x['order_id'], x['weight'], x['region'], x['delivery_hours'] = i
        data['data'].append(x)
    url = f'http://{HOST}:8080/orders'
    response = requests.post(url, json=data)
    if not response:
        print(response)
    print(response, response.json())


def edit_courier(c, *args):
    url = f'http://{HOST}:8080/couriers/' + str(c)
    data = {}
    for k, v in args:
        data[k] = v
    response = requests.patch(url, json=data)
    if not response:
        print(response)
    print(response, response.json())


def get_courier(c):
    url = f'http://{HOST}:8080/couriers/' + str(c)
    response = requests.get(url)
    if not response:
        print(response)
    print(response, response.json())


def assign_orders(c_id):
    url = f'http://{HOST}:8080/orders/assign'
    data = {
        'courier_id': c_id
    }
    print(requests.post(url, json=data).json())


def complete_orders(c_id, o_id, complete_t):
    url = f'http://{HOST}:8080/orders/complete'
    data = {
        'courier_id': c_id,
        'order_id': o_id,
        'complete_time': complete_t
    }
    print(requests.post(url, json=data).json())


test_url = f'http://{HOST}:8080/test'
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

# committed

# add_orders([3, 0.5, 13, ['11:00-13:30']]) passed
# assign_orders(1) passed
# complete_orders(1, 3, '2021-04-10T10:53:01.42Z') passed

# committed

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
# complete_orders(1, 12, '2021-03-18T21:36:00.680455Z') passed

# committed

# add_couriers([1, 'foot', [1, 12, 22], ['11:00-13:00', '18:00-22:00']]) passed
# edit_courier(1, ('regions', [13, 55])) passed
# assign_orders(1) passed
# complete_orders(1, 10, '2021-03-18T19:47:43.318541Z') passed
# complete_orders(1, 13, '2021-03-18T19:48:43.318541Z') passed

# committed
# add_couriers([1, 'foot', [1, 2, 3], ['16:00-18:00']]) passed
