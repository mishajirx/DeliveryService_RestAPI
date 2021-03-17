import datetime
import requests

test_url = 'http://127.0.0.1:5000/test'
print(requests.get(test_url).json())

# add couriers
url = 'http://127.0.0.1:5000/couriers'
data = {
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
}
# print(requests.post(url, json=data).json())
# add orders
url = 'http://127.0.0.1:5000/orders'
data = {
    "data": [
        {
            "order_id": 8,
            "weight": 15,
            "region": 22,
            "delivery_hours": ["09:00-18:00"]
        }
    ]
}
# print(requests.post(url, json=data).json())
# edit courier
url = 'http://127.0.0.1:5000/couriers/2'
data = {
    "regions": [11, 33, 2]
}
# print(requests.patch(url, json=data).json())
# assign orders
url = 'http://127.0.0.1:5000/orders/assign'
data = {
    'courier_id': 3,
}
# print(requests.post(url, json=data).json())
# complete_orders
url = 'http://127.0.0.1:5000/orders/complete'
data = {
    'courier_id': 3,
    'order_id': 8,
    'complete_time': "2021-03-17T23:53:01.42Z"
}
# print(requests.post(url, json=data).json())

url = 'http://127.0.0.1:5000/couriers/3'
print(requests.get(url).json())
