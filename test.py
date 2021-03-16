import requests

url = 'http://127.0.0.1:5000/test'


print(requests.get(url).json())
