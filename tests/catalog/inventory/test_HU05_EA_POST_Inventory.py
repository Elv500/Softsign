import pytest
import requests
import jsonschema

from faker import Faker

from utils.config import BASE_URL

faker = Faker()

@pytest.mark.smoke
def test_TC27_Crear_una_fuente_de_inventario_con_datos_validos(auth_headers):
    """
    Verificar que el sistema permite registrar correctamente una fuente nueva.
    """

    url = f"{BASE_URL}/admin/inventory-sources"

    payload = {
        "address": {
            "countryCode": "US",
            "street": "string",
            "city": "string",
            "postcode": "string"
        },
        "code": faker.slug(),
        "name": "string",
        "priority": 0,
        "channels": [
            "/api/v2/admin/channels/HOME_WEB"
        ]
    }

    response = requests.post(url, headers=auth_headers, json=payload)

    assert response.status_code == 201

    #Validacion Squema Input
    input_schema = {
        "type": "object",
        "required": [
            "address",
            "channels",
            "code",
            "name",
            "priority"
        ],
        "properties": {
            "address": {
                "type": "object",
                "required": [
                    "city",
                    "countryCode",
                    "postcode",
                    "street"
                ],
                "properties": {
                    "countryCode": {
                        "type": "string"
                    },
                    "street": {
                        "type": "string"
                    },
                    "city": {
                        "type": "string"
                    },
                    "postcode": {
                        "type": "string"
                    }
                }
            },
            "code": {
                "type": "string"
            },
            "name": {
                "type": "string"
            },
            "priority": {
                "type": "integer"
            },
            "channels": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    }

    try:
        jsonschema.validate(payload, input_schema)
    except jsonschema.ValidationError as e:
        pytest.fail(f"JSON schema input doesnt match {e}")


    #Validacion Schema output
    output_schema = {
        "type": "object",
        "required": [
            "@context",
            "@id",
            "@type",
            "address",
            "channels",
            "code",
            "id",
            "name",
            "priority"
        ],
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
            "address": {
                "type": "string"
            },
            "code": {
                "type": "string"
            },
            "name": {
                "type": "string"
            },
            "priority": {
                "type": "integer"
            },
            "channels": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    }

    try:
        jsonschema.validate(response.json(), output_schema)
    except jsonschema.ValidationError as e:
        pytest.fail(f"JSON schema output doesnt match {e}")