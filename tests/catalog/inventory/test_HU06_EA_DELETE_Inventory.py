import pytest
import time

from src.routes.request import SyliusRequest
from src.routes.endpoint_inventory import EndpointInventory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.assertions.inventory_assertions.inventory_errors_assertions import AssertionInventoryErrors
from src.data.inventory import generate_inventory_source_data
from utils.logger_helpers import log_request_response

#from src.routes.client import SyliusClient


# TC-32 – Admin > Catalog > Inventory - Eliminar Inventario existente con address y verificar eliminación del address asociado.
@pytest.mark.smoke
@pytest.mark.functional
def test_TC32_eliminar_inventory_existente_con_address(setup_create_inventory):
    headers, inventory = setup_create_inventory
    url = EndpointInventory.code(inventory["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response)
    log_request_response(url, response, headers, payload=inventory)


# TC-33 – Admin > Catalog > Inventory - Eliminar Inventario existente sin address.
@pytest.mark.smoke
@pytest.mark.functional
def test_TC33_eliminar_inventory_existente_sin_address(setup_create_inventory):
    headers, inventory = setup_create_inventory
    inventory["address"] = None
    url = EndpointInventory.code(inventory["code"])
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response)
    log_request_response(url, response, headers, payload=inventory)


# TC-34 – Admin > Catalog > Inventory - Verificar que Inventario eliminado no exista más.
@pytest.mark.functional
@pytest.mark.negative
def test_TC34_verificar_inventory_eliminado_no_exista(setup_create_inventory):
    headers, inventory = setup_create_inventory
    url = EndpointInventory.code(inventory["code"])
    response_delete = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response_delete)
    log_request_response(url, response_delete, headers, payload=inventory)
    response_get = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_404(response_get)
    log_request_response(url, response_get, headers)
    AssertionInventoryErrors.assert_inventory_error_request(response_get.json(), 404, "Not Found")


# TC-35 – Admin > Catalog > Inventory - Verificar que el address asociado no exista más después de eliminar el Inventario.
@pytest.mark.functional
@pytest.mark.xfail(reason="BUG35: Problemas con la construccion URL de Address", run=True)
def test_TC35_verificar_address_eliminado_despues_de_eliminar_inventory(setup_create_inventory):
    headers, inventory = setup_create_inventory
    url_inventory = EndpointInventory.code(inventory["code"])
    address_url = inventory.get("address")
    response_delete = SyliusRequest.delete(url_inventory, headers)
    AssertionStatusCode.assert_status_code_204(response_delete)
    log_request_response(url_inventory, response_delete, headers, payload=inventory)
    response_get_address = SyliusRequest.get(address_url, headers)
    AssertionStatusCode.assert_status_code_404(response_get_address)
    log_request_response(address_url, response_get_address, headers)


# TC-344 – Admin > Catalog > Inventory - Eliminar Inventario con código inexistente.
@pytest.mark.security
@pytest.mark.negative
def test_TC344_eliminar_inventory_codigo_inexistente(setup_create_inventory):
    headers, _ = setup_create_inventory
    codigo_inexistente = "codigo_inexistente"
    url = EndpointInventory.code(codigo_inexistente)
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    log_request_response(url, response, headers)
    AssertionInventoryErrors.assert_inventory_error_request(response.json(), 404, "Not Found")


# TC-345 – Admin > Catalog > Inventory - Eliminar Inventario sin token de autenticación.
@pytest.mark.security
@pytest.mark.negative
def test_TC345_eliminar_inventory_sin_token_autenticacion(setup_create_inventory):
    _, inventory = setup_create_inventory
    url = EndpointInventory.code(inventory["code"])
    response = SyliusRequest.delete(url, headers={})
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(url, response)
    AssertionInventoryErrors.assert_inventory_errors(response.json(), 401, "JWT Token not found")


# TC-346 – Admin > Catalog > Inventory - Eliminar Inventario con token inválido.
@pytest.mark.security
@pytest.mark.negative
def test_TC346_eliminar_inventory_con_token_invalido(setup_create_inventory):
    _, inventory = setup_create_inventory
    url = EndpointInventory.code(inventory["code"])
    headers_invalid = {"Authorization": "Bearer token_invalido"}
    response = SyliusRequest.delete(url, headers_invalid)
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(url, response, headers_invalid)
    AssertionInventoryErrors.assert_inventory_errors(response.json(), 401, "Invalid JWT Token")


# TC-347 – Admin > Catalog > Inventory - Eliminar Inventario con formato de código inválido.
@pytest.mark.security
@pytest.mark.negative
def test_TC347_eliminar_inventory_codigo_formato_invalido(setup_create_inventory):
    headers, _ = setup_create_inventory
    codigo_invalido = "   "
    url = EndpointInventory.code(codigo_invalido)
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    log_request_response(url, response, headers)
    AssertionInventoryErrors.assert_inventory_error_request(response.json(), 404, "Not Found")

#Revisar linea 109


# TC-348 – Admin > Catalog > Inventory - Eliminar Inventario con método HTTP incorrecto.
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.parametrize("metodo", ["get", "post", "put"])
def test_TC348_eliminar_inventory_metodo_http_incorrecto(setup_create_inventory, metodo):
    headers, inventory = setup_create_inventory
    url = EndpointInventory.code(inventory["code"])
    if metodo == "get":
        response = SyliusRequest.get(url, headers)
        AssertionStatusCode.assert_status_code_200(response)
    elif metodo == "post":
        response = SyliusRequest.post(url, headers)
        AssertionStatusCode.assert_status_code_405(response)
        log_request_response(url, response, headers)
    elif metodo == "put":
        response = SyliusRequest.put(url, headers, payload={})
        AssertionStatusCode.assert_status_code_200(response)
        log_request_response(url, response, headers)
    

# TC-349 – Admin > Catalog > Inventory - Eliminar Inventario dos veces consecutivamente.
@pytest.mark.negative
def test_TC349_eliminar_inventory_dos_veces(setup_create_inventory):
    headers, inventory = setup_create_inventory
    url = EndpointInventory.code(inventory["code"])
    response_delete_1 = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response_delete_1)
    log_request_response(url, response_delete_1, headers, payload=inventory)
    response_delete_2 = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(response_delete_2)
    log_request_response(url, response_delete_2, headers)


# TC-350 – Admin > Catalog > Inventory - Eliminar Inventario y verificar que no afecte otros Inventarios existentes.
@pytest.mark.functional
def test_TC350_eliminar_inventory_no_afecte_otros_inventory(setup_create_inventory):
    headers, inventory1 = setup_create_inventory
    payload2 = generate_inventory_source_data()
    url = EndpointInventory.inventory()
    inventario2_resp = SyliusRequest.post(url, headers, payload2)
    AssertionStatusCode.assert_status_code_201(inventario2_resp)
    inventario2 = inventario2_resp.json()
    log_request_response(url, inventario2_resp, headers, payload2)
    url1 = EndpointInventory.code(inventory1["code"])
    response_delete = SyliusRequest.delete(url1, headers)
    AssertionStatusCode.assert_status_code_204(response_delete)
    log_request_response(url1, response_delete, headers, payload=inventory1)
    url2 = EndpointInventory.code(inventario2["code"])
    response_get = SyliusRequest.get(url2, headers)
    AssertionStatusCode.assert_status_code_200(response_get)
    response_delete = SyliusRequest.delete(url2, headers)#Limpiando

# def test_TC351_eliminacion_concurrente_inventory(setup_create_inventory):


# TC-352 – Admin > Catalog > Inventory - Verificar que el tiempo de eliminar un Inventario sea menor a 3 segundos.
@pytest.mark.performance
def test_TC352_verificar_tiempo_respuesta_menor_3s_eliminar_inventory(setup_create_inventory):
    headers, inventory = setup_create_inventory
    url = EndpointInventory.code(inventory["code"])
    inicio = time.perf_counter()
    response = SyliusRequest.delete(url, headers)
    duracion = time.perf_counter() - inicio
    AssertionStatusCode.assert_status_code_204(response)
    AssertionInventoryErrors.assert_response_time_less_than(duracion, 3)