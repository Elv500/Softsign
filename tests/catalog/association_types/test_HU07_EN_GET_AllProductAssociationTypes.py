import jsonschema
import requests
import pytest
from utils.config import BASE_URL


def test_TC82_Obtener_todos_los_tipos_de_asociacion_de_producto_exitoso(auth_headers):

    url = f"{BASE_URL}/admin/product-association-types?page=1&itemsPerPage=10&order[code]=asc"

    response = requests.get(url, headers=auth_headers)

    schema = {
        "type": "object",
        "definitions": {
            "Translation": {
                "type": "object",
                "properties": {
                    "@id": {"type": "string"},
                    "@type": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["@id", "@type", "name"]
            },
            "Translations": {
                "type": "object",
                "properties": {
                    "en_US": {"$ref": "#/definitions/Translation"},
                    "de_DE": {"$ref": "#/definitions/Translation"},
                    "fr_FR": {"$ref": "#/definitions/Translation"},
                    "pl_PL": {"$ref": "#/definitions/Translation"},
                    "es_ES": {"$ref": "#/definitions/Translation"},
                    "es_MX": {"$ref": "#/definitions/Translation"},
                    "pt_PT": {"$ref": "#/definitions/Translation"},
                    "zh_CN": {"$ref": "#/definitions/Translation"}
                },
                "required": ["en_US"],
                "additionalProperties": False
            },
            "ProductAssociationTypeItem": {
                "type": "object",
                "properties": {
                    "@id": {"type": "string"},
                    "@type": {"type": "string"},
                    "id": {"type": "integer"},
                    "code": {"type": "string"},
                    "name": {"type": "string"},
                    "createdAt": {"type": "string"},
                    "updatedAt": {"type": "string"},
                    "translations": {"$ref": "#/definitions/Translations"}
                },
                "required": [
                    "@id", "@type", "id", "code",
                    "name", "createdAt", "updatedAt", "translations"
                ]
            },
            "HydraMappingItem": {
                "type": "object",
                "properties": {
                    "@type": {"type": "string"},
                    "variable": {"type": "string"},
                    "property": {"type": "string"},
                    "required": {"type": "boolean"}
                },
                "required": ["@type", "variable", "property", "required"]
            }
        },
        "properties": {
            "@context": {"type": "string"},
            "@id": {"type": "string"},
            "@type": {"type": "string"},
            "hydra:totalItems": {"type": "integer"},
            "hydra:member": {
                "type": "array",
                "items": {"$ref": "#/definitions/ProductAssociationTypeItem"}
            },
            "hydra:view": {
                "type": "object",
                "properties": {
                    "@id": {"type": "string"},
                    "@type": {"type": "string"}
                },
                "required": ["@id", "@type"]
            },
            "hydra:search": {
                "type": "object",
                "properties": {
                    "@type": {"type": "string"},
                    "hydra:template": {"type": "string"},
                    "hydra:variableRepresentation": {"type": "string"},
                    "hydra:mapping": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/HydraMappingItem"}
                    }
                },
                "required": [
                    "@type", "hydra:template",
                    "hydra:variableRepresentation", "hydra:mapping"
                ]
            }
        },
        "required": [
            "@context", "@id", "@type",
            "hydra:totalItems", "hydra:member",
            "hydra:view", "hydra:search"
        ]
    }

    assert response.status_code == 200
    try:
        jsonschema.validate(instance=response.json(), schema=schema)
    except jsonschema.ValidationError as err:
        pytest.fail("Response is not valid: {}".format(err))
