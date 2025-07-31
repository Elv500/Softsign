import jsonschema
import requests
import pytest
from faker import Faker
from utils.config import BASE_URL

faker = Faker()


def test_TC120_Crear_tipo_de_asociacion_con_code_y_translations_en_US_name_validos_exitoso(auth_headers):
    url = f"{BASE_URL}/admin/product-association-types"
    random_code = faker.uuid4()
    random_name = faker.company()

    data = {
        "code": random_code,
        "translations": {
            "en_US": {
                "name": random_name
            }
        }
    }

    schema_input = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "code": {
                "type": "string"
            },
            "translations": {
                "type": "object",
                "properties": {
                    "en_US": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string"
                            }
                        },
                        "required": ["name"]
                    },
                    "es_ES": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string"
                            }
                        }
                    },
                    "fr_FR": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string"
                            }
                        }
                    }
                },
                "required": ["en_US"],
                "additionalProperties": False
            }
        },
        "required": ["code", "translations"]
    }

    try:
        jsonschema.validate(instance=data, schema=schema_input)
    except jsonschema.ValidationError as err:
        pytest.fail(f"Input data is not valid: {err}")

    response = requests.post(url, headers=auth_headers, json=data)

    schema_output = {
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
        jsonschema.validate(instance=response.json(), schema=schema_output)
    except jsonschema.ValidationError as err:
        pytest.fail(f"Response is not valid: {err}")
