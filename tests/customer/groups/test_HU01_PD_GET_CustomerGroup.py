import jsonschema
import requests
import pytest

from utils.config import BASE_URL

@pytest.mark.smoke
@pytest.mark.regression
def test_TC117_Consultar_lista_de_Customer_Group_GET(auth_headers):
    """
    Verificar que la API devuelva correctamente el listado de todos los grupos de clientes. La respuesta
    debe contener un código HTTP 200 y la lista con objetos que representen cada grupo con sus datos completos.
    """
    url = f"{BASE_URL}/admin/customer-groups"

    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 200

    # Schema de salida JSON corregido
    schema = {
        "type": "object",
        "required": ["hydra:member"],
        "properties": {
            "hydra:member": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": { "type": "integer" },
                        "code": { "type": "string" },
                        "name": { "type": "string" }
                    },
                    "required": ["id", "code", "name"]
                }
            }
        }
    }

    # Validando schema de salida
    try:
        jsonschema.validate(instance=response.json(), schema=schema)
    except jsonschema.ValidationError as err:
        pytest.fail(f"Response is not valid: {err}")
