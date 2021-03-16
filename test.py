import requests

test_url = 'http://127.0.0.1:5000/test'
print(requests.get(test_url).json())

url = 'http://127.0.0.1:5000/couriers'

data = {
    "data": [
        {
            "courier_id": 2,
            "courier_type": "foot",
            "working_hours": ["11:35-14:05", "09:00-11:00"]
        }
    ]
}
print(requests.post(url, json=data).json())
