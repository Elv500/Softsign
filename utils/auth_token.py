import requests
from utils.config import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD

def get_token():
    url = f"{BASE_URL}/api/v2/admin/administrators/token"
    payload = {
        "email": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }

    response = requests.post(url, json=payload)
    return response.json()["token"]