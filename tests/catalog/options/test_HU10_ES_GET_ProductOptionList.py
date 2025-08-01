import jsonschema
import requests
import pytest

from utils.config import BASE_URL


@pytest.mark.smoke
@pytest.mark.funcional
def test_TC103_Validar_obtencion_exitosa_de_opciones_con_token_valido(auth_headers):
    """
    Verificar que la API devuelva correctamente el listado de todas las opciones de producto disponibles. La respuesta
    debe contener un código HTTP 200 y la lista con objetos que representen cada opción de productos con sus respectivos datos: Nombre y código.
    """
    url = f"{BASE_URL}/admin/product-options"

    response = requests.get (url, headers=auth_headers)
    assert response.status_code == 200
    #Schema de entrada JSON
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "hydra:member": {
                "type": "array",
                "items": {"$ref": "#/$defs/product_option"}
            }
        },
        "required": ["hydra:member"],
        "$defs": {
            "product_option": {
                "type": "object",
                "properties": {
                    "@id": {"type": "string"},
                    "@type": {"type": "string"},
                    "code": {"type": "string"},
                    "position": {"type": "integer"},
                    "values": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "translations": {
                        "type": "object",
                        "patternProperties": {
                            "^[a-z]{2}_[A-Z]{2}$": {
                                "type": "object",
                                "properties": {
                                    "@id": {"type": "string"},
                                    "@type": {"type": "string"},
                                    "name": {"type": "string"}
                                },
                                "required": ["@id", "@type", "name"]
                            }
                        },
                        "minProperties": 1  # Ajusta según requisitos mínimos
                    },
                    "createdAt": {"type": "string"},
                    "updatedAt": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": [
                    "@id", "@type", "code", "position", "values",
                    "translations", "createdAt", "updatedAt", "name"
                ]
            }
        }
    }

    #Validación de salida
    try:
        jsonschema.validate(instance=response.json(), schema=schema)
    except jsonschema.ValidationError as err:
        pytest.fail("Response is not valid: {}".format(err))