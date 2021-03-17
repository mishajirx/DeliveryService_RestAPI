import requests

test_url = 'http://127.0.0.1:5000/test'
print(requests.get(test_url).json())

url = 'http://127.0.0.1:5000/orders/assign'

data = {
    'courier_id': 2
}

print(requests.post(url, json=data).json())
