import jsonschema
import requests
import pytest

from utils.config import BASE_URL


@pytest.mark.smoke
@pytest.mark.regression
def test_TC36_Ver_listado_de_categorías_de_impuestos_exitosamente(auth_headers):
    """
    Verificar que la API devuelva correctamente el listado de todas las categorías de impuestos disponibles. La respuesta
    debe contener un código HTTP 200 y la lista con objetos que representen cada categoría con sus datos completos.
    """
    url = f"{BASE_URL}/admin/tax-categories"

    response = requests.get (url, headers=auth_headers)
    assert response.status_code == 200
    #Schema de entrada JSON
    schema = {
        "hydra:member": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "@id": {"type": "string"},
                    "@type": {"type": "string"},
                    "id": {"type": "integer"},
                    "code": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "createdAt": {"type": "string"},
                    "updatedAt": {"type": "string"}
                },
                "required": [
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
        }
    }
    #Validadndo schema de salida

    try:
        jsonschema.validate(instance=response.json(), schema=schema)
    except jsonschema.ValidationError as err:
        pytest.fail("Response is not valid: {}".format(err))


