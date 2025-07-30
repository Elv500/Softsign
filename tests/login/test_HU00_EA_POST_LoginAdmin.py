import requests
import pytest

import jsonschema
from jsonschema.exceptions import ValidationError

from utils.config import BASE_URL

@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.regression
def test_TC55_Login_exitoso_con_credenciales_validas():
    """
    Descripcion: El usuario puede iniciar sesion satisfactoriamente si ingresar credenciales validas
    """
    url = f"{BASE_URL}/admin/administrators/token"

    payload = {
        "email": "api@example.com",
        "password": "sylius-api"
    }
    
    response = requests.post(url, json=payload)
    assert response.status_code == 200

    #Esquema de entrada
    input_schema = {
        "type": "object",
        "required": [
            "email",
            "password"
        ],
        "properties": {
            "email": {
                "type": "string"
            },
            "password": {
                "type": "string"
            }
        }
    }
    #Validar la entrada del response con el equema de entrada
    try:
        jsonschema.validate(instance=payload, schema=input_schema)
    except ValidationError as err:
        pytest.fail(f"JSON schema input doesnt match {err}")
        
    #Esquema de salida
    output_schema = {
        "type": "object",
        "required": [
            "adminUser",
            "token"
        ],
        "properties": {
            "token": {
                "type": "string"
            },
            "adminUser": {
                "type": "string"
            }
        }
    }
    #Validar la salida del response con el equema de salida
    try:
        jsonschema.validate(instance=response.json(), schema=output_schema)
    except ValidationError as err:
        pytest.fail(f"JSON schema output doesnt match {err}")