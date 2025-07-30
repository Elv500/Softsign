import jsonschema
import requests
import pytest
from utils.config import BASE_URL


def test_TC120_Crear_tipo_de_asociacion_con_code_y_translations_en_US_name_validos_exitoso(auth_headers):
    url = f"{BASE_URL}/admin/product-association-types"
    data = {
        "code": "MtJHPlPVc8LsrLQdZSTD-3NrEBA_BWr_XYZ2",
        "translations": {
            "en_US": {
                "name": "Colgate"
            }
        }
    }
    response = requests.post(url, headers=auth_headers, json=data)

    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "@context": {"type": "string"},
            "@id": {"type": "string"},
            "@type": {"type": "string"},
            "id": {"type": "integer"},
            "code": {"type": "string"},
            "name": {"type": "string"},
            "createdAt": {"type": "string"},
            "updatedAt": {"type": "string"},
            "translations": {
                "type": "object",
                "properties": {
                    "en_US": {
                        "type": "object",
                        "properties": {
                            "@id": {"type": "string"},
                            "@type": {"type": "string"},
                            "name": {"type": "string"}
                        },
                        "required": ["@id", "@type", "name"]
                    }
                },
                "required": ["en_US"]
            }
        },
        "required": [
            "@context",
            "@id",
            "@type",
            "id",
            "code",
            "name",
            "createdAt",
            "updatedAt",
            "translations"
        ]
    }

    assert response.status_code == 201
    try:
        jsonschema.validate(instance=response.json(), schema=schema)
    except jsonschema.ValidationError as err:
        pytest.fail(f"Response is not valid: {err}")
