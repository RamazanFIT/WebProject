import requests



def send_log(username, password):
    url = 'http://127.0.0.1:8000/api/authorization/login/'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': 'rnfIjTXipfWpoMOMR4uyIX5wQbmiwSqnfdsNm4x9l7Y3lzp4UaqdcVIgkunSFAoq',
    }
    data = {
        "username": username,
        "password": password,
        'q' : 12
    }

    requests.post(url, headers=headers, json=data)
