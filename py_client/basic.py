import requests

url = 'http://localhost:8000/api/'


r = requests.get(url=url)

print(r.json().get('message'), r.status_code)