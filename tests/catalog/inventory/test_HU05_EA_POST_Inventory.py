import pytest

from src.assertions.inventory_assertions import AssertionInventory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_inventory import EndpointInventory
from src.routes.request import SyliusRequest
from src.data.inventory import generate_inventory_source_data

@pytest.mark.smoke
def test_TC27_Crear_una_fuente_de_inventario_con_datos_validos(auth_headers):
    
    data = generate_inventory_source_data()
    response = SyliusRequest.post(EndpointInventory.inventory(), auth_headers, data)
    AssertionInventory.assert_inventory_add_input_schema(data)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionInventory.assert_inventory_add_output_schema(response.json())
    created_inventory = response.json()
    created_inventories.append(created_inventory)
