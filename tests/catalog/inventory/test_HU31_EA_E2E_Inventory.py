import pytest


from src.routes.request import SyliusRequest
from src.routes.endpoint_inventory import EndpointInventory
from src.assertions.status_code_assertions import AssertionStatusCode
from utils.logger_helpers import log_request_response
from src.data.inventory import generate_inventory_source_data


# TC-355: Admin > Inventory - Autenticarse con credenciales válidas y obtener token.
# TC-356: Admin > Inventory - Listar inventarios con autenticación válida.
# TC-357: Admin > Inventory - Crear un inventario válido satisfactoriamente.
# TC-358: Admin > Inventory - Obtener el inventario recién creado.
# TC-359: Admin > Inventory - Editar el inventario creado satisfactoriamente.
# TC-360: Admin > Inventory - Eliminar el inventario creado satisfactoriamente.
@pytest.mark.e2e
@pytest.mark.inventory
@pytest.mark.high
def test_TC355_a_TC360_End_To_End_Inventory(setup_e2e_inventory):
    
    #TC-355: Admin > Inventory - Autenticarse con credenciales válidas y obtener token.
    headers, created_inventories = setup_e2e_inventory
    
    #Limites - Si el modulo tiene muchos elementos se pone un limite de muestra (<=2)
    params = {"itemsPerPage": 2}

    #TC-356: Admin > Inventory - Listar inventarios con autenticación válida.
    url = EndpointInventory.inventory_with_params(**params)
    responseGet = SyliusRequest.get(url, headers)
    log_request_response(url, responseGet, headers)
    
    #TC-357: Admin > Inventory - Crear un inventario válido satisfactoriamente.
    payloadPost = generate_inventory_source_data()
    url = EndpointInventory.inventory()
    responsePost = SyliusRequest.post(url, headers, payloadPost)
    log_request_response(url, responsePost, headers, payloadPost)
    
    #Teardown - Por si falla en algun paso, se hace limpieza.
    inventory = responsePost.json()
    created_inventories.append(responsePost)

    #TC-358: Admin > Inventory - Obtener el inventario recién creado.
    url = EndpointInventory.code(inventory['code'])
    responseGetId = SyliusRequest.get(url, headers)
    log_request_response(url, responseGetId, headers)
    
    #TC-359: Admin > Inventory - Editar el inventario creado satisfactoriamente.
    payloadPut = generate_inventory_source_data()
    url = EndpointInventory.code(inventory['code'])
    responsePut = SyliusRequest.put(url, headers, payloadPut)
    log_request_response(url, responsePut, headers, payloadPut)
    
    #TC-360: Admin > Inventory - Eliminar el inventario creado satisfactoriamente.
    url = EndpointInventory.code(inventory['code'])
    responseDelete = SyliusRequest.delete(url, headers)
    log_request_response(url, responseDelete, headers)
    AssertionStatusCode.assert_status_code_204(responseDelete)