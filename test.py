import datetime
import argparse
import requests

# HOST = '0.0.0.0'
HOST = '127.0.0.1'
parser = argparse.ArgumentParser(  # объект обрабатывающий аргументы(как в функции)
    description="convert integers to decimal system")
parser.add_argument('--clear', default='0', type=str, help='need to delete all data?(yes(1)/no(0))')


def check_assign_time(j1: dict, j2: dict):
    t1 = j1['assign_time']
    t2 = j2['assign_time']
    u = datetime.datetime.fromisoformat(t1.split('.')[0])
    v = datetime.datetime.fromisoformat(t2.split('.')[0])
    if (u - v).total_seconds() <= 1:
        return True
    return False


# methods for comfortable testing
def add_couriers(data) -> requests.models.Response:
    url = f'http://{HOST}:8080/couriers'
    response = requests.post(url, json=data)
    # print(response, response.json())
    return response


def add_orders(data) -> requests.models.Response:
    url = f'http://{HOST}:8080/orders'
    response = requests.post(url, json=data)
    # print(response, response.json())
    return response


def edit_courier(courier_id, data) -> requests.models.Response:
    url = f'http://{HOST}:8080/couriers/' + str(courier_id)
    response = requests.patch(url, json=data)
    # if not response:
    #     print(response)
    # else:
    #     print(response, response.json())
    return response


def get_courier(courier_id) -> requests.models.Response:
    url = f'http://{HOST}:8080/couriers/' + str(courier_id)
    response = requests.get(url)
    if not response:
        print(response)
    else:
        print(response, response.json())
    return response


def assign_orders(courier_id):
    url = f'http://{HOST}:8080/orders/assign'
    data = {'courier_id': courier_id}
    response = requests.post(url, json=data)
    if not response:
        print(response)
    else:
        print(response, response.json())
    return response


def complete_orders(data):
    url = f'http://{HOST}:8080/orders/complete'
    response = requests.post(url, json=data)
    if not response:
        print(response)
    else:
        print(response, response.json())


def clear_db(data):
    url = f'http://{HOST}:8080/clear'
    response = requests.post(url, json=data)
    print(response, response.json())


"""Тест соединения"""


def test_connection():
    try:
        test_url = f'http://{HOST}:8080/test'
        response = requests.get(test_url)
        if response:
            print(response.json())
        else:
            print(response)
        clear_db({'code': 'zhern0206eskiy'})
    except requests.exceptions.ConnectionError as e:
        print('Something went wrong: Connection Error')
        print('Try to rerun service')
        exit(0)


""" Основные тесты"""


def test_post_couriers_normal_data():
    res = add_couriers({
        "data": [
            {
                "courier_id": 1,
                "courier_type": "foot",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            },
            {
                "courier_id": 2,
                "courier_type": "bike",
                "regions": [22],
                "working_hours": ["09:00-18:00"]
            },
            {
                "courier_id": 3,
                "courier_type": "car",
                "regions": [12, 22, 23, 33],
                "working_hours": ['22:00-22:30']
            }
        ]
    })  # добавление курьеров (нормальные данные)
    assert res.status_code == 201 and res.json() == {'couriers': [{'id': 1}, {'id': 2}, {'id': 3}]}
    # {'couriers': [{'id': 1}, {'id': 2}, {'id': 3}]}


def test_post_couriers_repeating_id():
    res = add_couriers({
        "data": [
            {
                "courier_id": 1,
                "courier_type": "foot",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            },
            {
                "courier_id": 2,
                "courier_type": "bike",
                "regions": [22],
                "working_hours": ["09:00-18:00"]
            },
            {
                "courier_id": 3,
                "courier_type": "car",
                "regions": [12, 22, 23, 33],
                "working_hours": []
            }
        ]
    })  # повторение айдишников (ошибка)
    assert res.status_code == 400 and res.json() == {'validation_error': [{'id': 1}, {'id': 2}, {'id': 3}]}
    # {'validation_error': [{'id': 1}, {'id': 2}, {'id': 3}]}


def test_post_couriers_wrong_field():
    res = add_couriers({
        "data": [
            {
                "courier_id": 5,
                "courier_type": "foot",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            },
            {
                "courier_id": 7,
                "courier_type": "bike",
                "regions": [22],
                "working_hours": ["09:00-18:00"]
            },
            {
                "courier_id": 9,
                "courier_type": "car",
                "regions": [12, 22, 23, 33],
                "working_hours": [],
                "foo": 2
            }
        ]
    })  # несуществующее поле (ошибка)
    assert res.status_code == 400 and res.json() == {'validation_error': [{'id': 9}]}
    # {'validation_error': [{'id': 9}]}


def test_post_couriers_missing_field():
    res = add_couriers({
        "data": [
            {
                "courier_id": 5,
                "courier_type": "foot",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            },
            {
                "courier_id": 7,
                "courier_type": "bike",
                "working_hours": ["09:00-18:00"]
            },
            {
                "courier_id": 9,
                "courier_type": "car",
                "regions": [12, 22, 23, 33],
                "working_hours": [],
            }
        ]
    })  # отсутствие поля (ошибка)
    assert res.status_code == 400 and res.json() == {'validation_error': [{'id': 7}]}
    # {'validation_error': [{'id': 7}]}


def test_patch_couriers_all_params():
    res = edit_courier(1, {
        "regions": [11, 33, 2],
        "working_hours": ['12:00-12:30'],
        'courier_type': 'car'
    })  # изменение всех параметров (нормальные данные)
    assert res.status_code == 200 and res.json() == {'courier_id': '1', 'courier_type': 'foot', 'regions': [11, 33, 2],
                                                     'working_hours': ['12:00-12:30']}


def test_patch_couriers_any_params():
    res = edit_courier(1, {
        "regions": [11, 2],
        "working_hours": ['11:00-15:30'],
    })  # изменение не всех параметров (нормальные данные)
    assert res.status_code == 200 and res.json() == {'courier_id': '1', 'courier_type': 'foot', 'regions': [11, 2],
                                                     'working_hours': ['11:00-15:30']}


def test_patch_couriers_wrong_params():
    res = edit_courier(1, {
        'bar': 123
    })  # изменение несуществующего параметра (ошибка)
    assert res.status_code == 400


def test_post_orders_normal_data():
    res = add_orders({
        "data": [
            {
                "order_id": 1,
                "weight": 0.23,
                "region": 12,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 2,
                "weight": 15,
                "region": 1,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 3,
                "weight": 0.01,
                "region": 22,
                "delivery_hours": ["09:00-12:00", "16:00-21:30"]
            }
        ]
    })  # добавление заказов (нормальные данные)
    assert res.status_code == 201 and res.json() == {'orders': [{'id': 1}, {'id': 2}, {'id': 3}]}


def test_post_orders_repeating_id():
    res = add_orders({
        "data": [
            {
                "order_id": 5,
                "weight": 0.23,
                "region": 12,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 8,
                "weight": 15,
                "region": 1,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 3,
                "weight": 0.01,
                "region": 22,
                "delivery_hours": ["09:00-12:00", "16:00-21:30"]
            }
        ]
    })  # повторение айди (ошибка)
    assert res.status_code == 400 and res.json() == {'validation_error': [{'id': 3}]}


def test_post_orders_missing_field():
    res = add_orders({
        "data": [
            {
                "order_id": 1,
                "weight": 0.23,
                "region": 12,
                "delivery_hours": ["09:00-18:00"],
                "fjhfbgudrgbdiu": 123
            },
            {
                "order_id": 2,
                "weight": 15,
                "region": 1,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 3,
                "weight": 0.01,
                "region": 22,
                "delivery_hours": ["09:00-12:00", "16:00-21:30"]
            }
        ]
    })  # несуществующее поле (ошибка)
    assert res.status_code == 400 and res.json() == {'validation_error': [{'id': 1}, {'id': 2}, {'id': 3}]}


def test_post_orders_too_big_weight():
    res = add_orders({
        "data": [
            {
                "order_id": 10,
                "weight": 100,
                "region": 12,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 11,
                "weight": 15,
                "region": 1,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 12,
                "weight": 0.01,
                "region": 22,
                "delivery_hours": ["09:00-12:00", "16:00-21:30"]
            }
        ]
    })  # слишком большой вес (ошибка)
    assert res.status_code == 400 and res.json() == {'validation_error': [{'id': 10}]}


def test_post_orders_too_small_weight():
    res = add_orders({
        "data": [
            {
                "order_id": 10,
                "weight": 0.00001,
                "region": 12,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 11,
                "weight": 15,
                "region": 1,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 12,
                "weight": 0.01,
                "region": 22,
                "delivery_hours": ["09:00-12:00", "16:00-21:30"]
            }
        ]
    })  # слишком маленький вес (ошибка)
    assert res.status_code == 400 and res.json() == {'validation_error': [{'id': 10}]}


def test_assign_orders_courier_with_some_orders():
    res = assign_orders(1)  # назначение заказов курьеру 1 (нормальные данные)
    assert res.status_code == 200 and res.json() == {'orders': []}


def test_assign_orders_courier_without_orders():
    res = assign_orders(2)  # назначение заказов курьеру 2 (нормальные данные)
    t = str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    assert res.status_code == 200 and check_assign_time(res.json(), {'assign_time': t, 'orders': [{'id': 3}]})


def test_assign_orders_wrong_courier():
    res = assign_orders(4)  # назначение заказов курьеру 3 (ошибка)
    assert res.status_code == 400


def test_assign_orders_idempotent_proof():
    res1 = assign_orders(2)  # назначение заказов курьеру 2 (нормальные данные)
    res2 = assign_orders(2)
    t = str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    assert res1.status_code == res2.status_code == 201 and \
           check_assign_time(res1.json(), res2.json()) and \
           check_assign_time(res1.json(), {'assign_time': t, 'orders': [{'id': 3}]}) and \
           check_assign_time(res2.json(), {'assign_time': t, 'orders': [{'id': 3}]})


def test_complete_orders():
    complete_orders({
        "courier_id": 2,
        "order_id": 3,
        "complete_time": str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    })  # выполнение курьером 2 заказа 3 (нормальные данные)
    complete_orders({
        "courier_id": 2,
        "order_id": 3,
        "complete_time": str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    })  # выполнение курьером 2 заказа 3 (нормальные данные) доказываем идемпотентность
    complete_orders({
        "courier_id": 1,
        "order_id": 3,
        "complete_time": str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    })  # выполнение курьером 1 заказа 3 (ошибка)
    complete_orders({
        "courier_id": 2,
        "order_id": 1,
        "complete_time": str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    })  # выполнение курьером 2 заказа 1 (ошибка)
    complete_orders({
        "courier_id": 4,
        "order_id": 5,
        "complete_time": str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    })  # выполнение курьером 4 заказа 5 (ошибка)


def test_get_courier_with_some_orders():
    res = get_courier(3)  # информация о курьере 3 (нормальные данные)
    assert res.status_code == 201 and \
           res.json() == {'courier_id': '3', 'courier_type': 'car', 'earnings': 0, 'regions': [12, 22, 23, 33],
                          'working_hours': ['22:00-22:30']}


def test_get_courier_without_any_orders():
    res = get_courier(2)  # информация о курьере 2 (нормальные данные)
    assert res.status_code == 201


def test_get_courier_wrong_id():
    res = get_courier(4)  # информация о курьере 4 (ошибка)
    assert res.status_code == 400


""" Тест на то что при изменение данных о курьере заказ может стать свободным """


def test_orders_leaving():
    add_orders({
        "data": [
            {
                "order_id": 4,
                "weight": 40,
                "region": 22,
                "delivery_hours": ["22:00-22:15"]
            }
        ]
    })  # добавили заказ с весом 40 (норм)
    assign_orders(3)  # назначили его курьеру на машине (норм)
    edit_courier(3, {'courier_type': 'foot'})  # он поменял тип (норм)
    complete_orders({
        "courier_id": 3,
        "order_id": 4,
        "complete_time": str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    })  # заказ больше не его (ошибка)
    edit_courier(3, {'courier_type': 'car'})  # меняем обратно (ок)
    assign_orders(3)  # назначили его курьеру с подходящим временем (ок)
    edit_courier(3, {'working_hours': ['12:00-13:00']})  # он поменял рабочее время (ок)
    complete_orders({
        "courier_id": 3,
        "order_id": 4,
        "complete_time": str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    })  # заказ больше не его (ошибка)
    edit_courier(3, {'working_hours': ['22:00-22:30']})  # меняем обратно (ок)
    assign_orders(3)  # назначили его курьеру с подходящим регионом (ок)
    edit_courier(3, {'regions': [1]})  # он поменял рабочее время (ок)
    complete_orders({
        "courier_id": 3,
        "order_id": 4,
        "complete_time": str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    })  # заказ больше не его (ошибка)


"""Тест на то что нельзя забрать уже назначенный заказ"""


def test_orders_are_not_for_many_couriers():
    add_couriers({
        "data": [
            {
                "courier_id": 6,
                "courier_type": "bike",
                "regions": [40],
                "working_hours": ["13:00-13:50"]
            },
            {
                "courier_id": 7,
                "courier_type": "bike",
                "regions": [40],
                "working_hours": ["13:00-13:50"]
            }
        ]
    })  # создадим двух почти одинаковых курьеров
    # {'couriers': [{'id': 6}, {'id': 7}]}
    add_orders({
        "data": [
            {
                "order_id": 8,
                "weight": 10,
                "region": 40,
                "delivery_hours": ["13:30-13:41"]
            }
        ]
    })  # добавим подходящий им заказ
    assign_orders(6)  # один его получит
    assign_orders(7)  # второй нет
    complete_orders({
        "courier_id": 6,
        "order_id": 8,
        "complete_time": str(datetime.datetime.utcnow()).replace(' ', 'T') + 'Z'
    })  # выполняет заказ
    assign_orders(7)  # второй также не может получить его

# args = parser.parse_args()
# test_connection()
# if args.clear[0] == '1':
#     code = 'zhern0206eskiy'
#     # code = input('write password to access you clear data: ')
#     clear_db({'code': code})
