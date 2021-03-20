import datetime
import argparse
import requests

HOST = '127.0.0.1'
parser = argparse.ArgumentParser(  # объект обрабатывающий аргументы(как в функции)
    description="convert integers to decimal system")
parser.add_argument('--clear', default='0', type=str, help='need to delete all data?(yes(1)/no(0))')


# methods for comfortable testing
def add_couriers(data):
    url = f'http://{HOST}:8080/couriers'
    response = requests.post(url, json=data)
    (response, response.json())


def add_orders(data):
    url = f'http://{HOST}:8080/orders'
    response = requests.post(url, json=data)
    print(response, response.json())


def edit_courier(courier_id, data):
    url = f'http://{HOST}:8080/couriers/' + str(courier_id)
    response = requests.patch(url, json=data)
    if not response:
        print(response)
    else:
        print(response, response.json())


def get_courier(courier_id):
    url = f'http://{HOST}:8080/couriers/' + str(courier_id)
    response = requests.get(url)
    if not response:
        print(response)
    else:
        print(response, response.json())


def assign_orders(data):
    url = f'http://{HOST}:8080/orders/assign'
    response = requests.post(url, json=data)
    if not response:
        print(response)
    else:
        print(response, response.json())


def complete_orders(data, complete_t):
    url = f'http://{HOST}:8080/orders/complete'
    response = requests.post(url, json=data)
    if not response:
        print(response)
    else:
        print(response, response.json())


def test_connection():
    try:
        test_url = f'http://{HOST}:8080/test'
        response = requests.get(test_url)
        if response:
            print(response.json())
        else:
            print(response)
    except requests.exceptions.ConnectionError as e:
        print('Something went wrong: Connection Error')
        print('Try to rerun service')
        exit(0)


def clear_db(data):
    url = f'http://{HOST}:8080/clear'
    response = requests.post(url, json=data)
    print(response, response.json())


"""TEST HISTORY"""
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

# COMMITTED

# add_orders([3, 0.5, 13, ['11:00-13:30']]) passed
# assign_orders(1) passed
# complete_orders(1, 3, '2021-04-10T10:53:01.42Z') passed

# COMMITTED

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

# COMMITTED

# add_couriers([1, 'foot', [1, 12, 22], ['11:00-13:00', '18:00-22:00']]) passed
# edit_courier(1, ('regions', [13, 55])) passed
# assign_orders(1) passed
# complete_orders(1, 10, '2021-03-18T19:47:43.318541Z') passed
# complete_orders(1, 13, '2021-03-18T19:48:43.318541Z') passed

# COMMITTED

# add_couriers([1, 'foot', [1, 2, 3], ['16:00-18:00']]) passed

# COMMITTED - new testing system. Now need to give all data dictionary
args = parser.parse_args()
test_connection()
if args.clear[0] == '1':
    code = input('write password to access you clear data: ')
    clear_db({'code': code})
