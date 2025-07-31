import requests
import pytest
import jsonschema

from utils.config import BASE_URL

@pytest.mark.smoke
@pytest.mark.regression
def test_TC23_Obtener_lista_completa_de_fuentes_de_inventario(auth_headers):
    """
    Verificar que el sistema retorna correctamente el listado de fuentes registradas.
    """

    url = f"{BASE_URL}/admin/inventory-sources"

    response = requests.get(url, headers=auth_headers)

    assert response.status_code == 200

    #Validando esquema
    schema = {
        "type": "object",
        "required": [
            "@context",
            "@id",
            "@type",
            "hydra:member",
            "hydra:totalItems"
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
            "hydra:totalItems": {
                "type": "integer"
            },
            "hydra:member": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
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
                            "type": "null"
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
                    },
                    "required": [
                        "@id",
                        "@type",
                        "address",
                        "channels",
                        "code",
                        "id",
                        "name",
                        "priority"
                    ]
                }
            }
        }
    }

    try:
        jsonschema.validate(response.json(), schema)
    except jsonschema.ValidationError as e:
        pytest.fail(f"JSON schema output doesnt match {e}")