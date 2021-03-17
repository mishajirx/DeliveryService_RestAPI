import requests

test_url = 'http://127.0.0.1:5000/test'
print(requests.get(test_url).json())

url = 'http://127.0.0.1:5000/orders/complete'

data = {
    'courier_id': 2,
    'order_id': 1,
    'complete_time': "2021-01-10T10:33:01.42Z"
}

print(requests.post(url, json=data).json())
