import requests
import pytest
import jsonschema
import json
from utils.config import BASE_URL


def test_TC13_Admin_Customer_Group_Verificar_código_de_respuesta_201_Created(auth_headers):
    """
    Validar que la API permita crear un Customer Group cuando se envían datos válidos devolviendo el codigo 201 POST.
    """
    url = f"{BASE_URL}/admin/customer-groups"

    payload ={
        "code": "Test_Codes3",
        "name": "Prueba"
    }
    # Validacion del codigo de respuesta de la API
    response = requests.post(url, json=payload, headers=auth_headers)
    assert response.status_code == 201



    # Validando el esquema de entrada
    # El esquema de entrada debe coincidir con el payload enviado
    # y debe contener los campos "code" y "name"
    input_schema = {
        "type": "object",
        "properties": {
            "code": {
            "type": "string"
            },
            "name": {
            "type": "string"
            }
        },
        "required": [
            "code",
            "name"
        ]
    }
    try:
        jsonschema.validate(response.json(), input_schema)
    except jsonschema.ValidationError as err:
        pytest.fail("Response is not valid: {}".format(err))



    # Validando el esquema de salida
    #validando schema
    output_schema = {
        "type": "object",
        "properties": {
            "@context": {
            "type": "string"
            },
            "@id": {
            "type": "string"
            },
            "@type": {
            "type": "string"
            },
            "id": {
            "type": "integer"
            },
            "code": {
            "type": "string"
            },
            "name": {
            "type": "string"
            }
        },
        "required": [
            "@context",
            "@id",
            "@type",
            "id",
            "code",
            "name"
        ]
    }
    try:
        jsonschema.validate(response.json(), output_schema)
    except jsonschema.ValidationError as err:
        pytest.fail("Response is not valid: {}".format(err))