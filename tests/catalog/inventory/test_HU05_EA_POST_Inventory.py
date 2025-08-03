import pytest

from src.assertions.inventory_assertions import AssertionInventory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_inventory import EndpointInventory
from src.routes.request import SyliusRequest
from src.data.inventory import generate_inventory_source_data
from utils.logger_helpers import log_request_response

@pytest.mark.smoke
def test_TC27_Crear_una_fuente_de_inventario_con_datos_validos(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionInventory.assert_inventory_add_output_schema(response.json())

    log_request_response(url, headers, response, payload)

    created_inventory = response.json()
    created_inventories.append(created_inventory)