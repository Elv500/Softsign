import requests
from utils.config import BASE_URL

def test_succesfully_access():
    """
    Iniciar sesión exitosamente con credenciales validas
    """
    url = f"{BASE_URL}/admin/administrators/token"

    payload ={
        "email": "api@example.com",
        "password": "sylius-api"
    }
    response = requests.post(url, json=payload)

    assert response.status_code == 200