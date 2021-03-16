import requests


def is_time_ok(t1, t2) -> bool:
    # format HH:MM - HH:MM
    b1, b2 = t1.split(' - ')
    start1 = b1.split(':')
    start1 = int(start1[0]) * 60 + int(start1[1])
    end1 = b2.split(':')
    end1 = int(end1[0]) * 60 + int(end1[1])
    b1, b2 = t2.split(' - ')
    start2 = b1.split(':')
    start2 = int(start2[0]) * 60 + int(start2[1])
    end2 = b2.split(':')
    end2 = int(end2[0]) * 60 + int(end2[1])
    if max(start1, start2) <= min(end1, end2):
        return True
    return False


print(is_time_ok('16:00 - 18:00', '18:00 - 19:00'))
test_url = 'http://127.0.0.1:5000/test'
print(requests.get(test_url).json())

url = 'http://127.0.0.1:5000/couriers/2'

data = {
    "regions": [11, 33, 2]
}

print(requests.patch(url, json=data).json())

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
        },
    ]
}
# print(requests.post(url, json=data).json())
