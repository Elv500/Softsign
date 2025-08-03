import pytest
import logging

from src.assertions.inventory_assertions import AssertionInventory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_inventory import EndpointInventory
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response

@pytest.mark.smoke
@pytest.mark.regression
def test_TC23_Obtener_lista_completa_de_fuentes_de_inventario(auth_headers):
    url = EndpointInventory.inventory()
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionInventory.assert_inventory_list_schema(response.json())
    log_request_response(url, auth_headers, response)