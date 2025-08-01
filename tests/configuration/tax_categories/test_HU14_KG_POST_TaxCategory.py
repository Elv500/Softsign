import requests
import pytest
import jsonschema
import json
from utils.config import BASE_URL


def test_TC60_Crear_categoría_de_impuesto_exitosamente(auth_headers):
    """
    Validar que la API permita crear una categoría de impuesto cuando se envían datos válidos.
    """
    url = f"{BASE_URL}/admin/tax-categories"

    payload ={
        "code": "12452-jsbljsdbvlkjsbc",
        "name": "huevos",
        "description": "Ventas de huevos"
    }

    response = requests.post(url, json=payload, headers=auth_headers)
    assert response.status_code == 201




    input_schema = {
      "type": "object",
      "properties": {
        "code": {
          "type": "string"
        },
        "name": {
          "type": "string"
        },
        "description": {
          "type": "string"
        }
      },
      "required": [
        "code",
        "name",
        "description"
      ]
    }
    try:
        jsonschema.validate(response.json(), input_schema)
    except jsonschema.ValidationError as err:
        pytest.fail("Response is not valid: {}".format(err))




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
        },
        "description": {
          "type": "string"
        },
        "createdAt": {
          "type": "string"
        },
        "updatedAt": {
          "type": "string"
        }
      },
      "required": [
        "@context",
        "@id",
        "@type",
        "id",
        "code",
        "name",
        "description",
        "createdAt",
        "updatedAt"
      ]
    }
    try:
        jsonschema.validate(response.json(), output_schema)
    except jsonschema.ValidationError as err:
        pytest.fail("Response is not valid: {}".format(err))
