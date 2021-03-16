import requests

test_url = 'http://127.0.0.1:5000/test'
print(requests.get(test_url).json())

url = 'http://127.0.0.1:5000/orders'

data = {
    "data": [
        {
            "order_id": 6,
            "weight": 0.68,
            "delivery_hours": ["09:00-18:00"]
        },
    ]
}

print(requests.post(url, json=data).json())
