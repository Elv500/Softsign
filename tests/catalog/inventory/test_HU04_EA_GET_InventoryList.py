import pytest

from src.assertions.inventory_assertions import AssertionInventory
from src.assertions.status_code_assertions import AssertionStatusCode
from utils.config import BASE_URL

@pytest.mark.smoke
@pytest.mark.regression
def test_TC23_Obtener_lista_completa_de_fuentes_de_inventario(auth_headers):

    url = f"{BASE_URL}/admin/inventory-sources"
    response = requests.get(url, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionInventory.assert_inventory_list_schema(response.json())