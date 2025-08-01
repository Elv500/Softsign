import jsonschema
import requests
import pytest

from utils.config import BASE_URL

@pytest.mark.smoke
@pytest.mark.regression
def test_TC38_Obtener_el_listado_de_atributos_en_el_sistema_Sylius(auth_headers):
    """ Verificar que el metodo GET devuelva la lista de todos los atributos registrados en la submenu Sylius.
    La respuesta debe contener un código HTTP 200 y la lista de atributes
    """
    url = f"{BASE_URL}/admin/product-attributes"
    response = requests.get(url, headers=auth_headers, timeout=10)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Body: {response.text}"
    # Schema de response JSON
    schema = {
        "type": "object",
        "required": ["hydra:member"],
        "properties": {
            "hydra:member": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["@id", "@type", "code", "type", "translations"],
                    "properties": {
                        "@id": {"type": "string"},
                        "@type": {"type": "string"},
                        "code": {"type": "string"},
                        "type": {"type": "string"},
                        "configuration": {"type": ["array", "object"]},
                        "storageType": {"type": "string"},
                        "position": {"type": "integer"},
                        "translatable": {"type": "boolean"},
                        "translations": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "object",
                                "required": ["name"],
                                "properties": {
                                    "@id": {"type": "string"},
                                    "@type": {"type": "string"},
                                    "name": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    try:
        jsonschema.validate(instance=response.json(), schema=schema)
    except jsonschema.ValidationError as err:
        pytest.fail(f"Schema validation failed: {err}")

    attributes = response.json()["hydra:member"]
    assert len(attributes) > 0, "La lista de atributos está vacía"
