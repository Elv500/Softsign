import pytest

from src.assertions.inventory_assertions.inventory_schema_assertions import AssertionInventory
from src.assertions.inventory_assertions.inventory_post_content_assertions import AssertionInventoryCreate
from src.assertions.inventory_assertions.inventory_errors_assertions import AssertionInventoryErrors
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_inventory import EndpointInventory
from src.routes.request import SyliusRequest
from src.data.inventory import generate_inventory_source_data, create_inventory_data
from utils.logger_helpers import log_request_response

#from src.routes.client import SyliusClient


# TC-27 – Admin > Catalog > Inventory - Crear inventory con todos los campos válidos.
@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.high
def test_TC27_crear_inventory_con_todos_los_campos_validos(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    AssertionInventoryCreate.assert_inventory_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_inventories.append(response_json)


# TC-28 – Admin > Catalog > Inventory - Crear inventory solo con campos requeridos.
@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.high
def test_TC28_crear_inventory_con_campos_requeridos(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data(required_only=True)
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload, required_only=True)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    AssertionInventoryCreate.assert_inventory_response(payload, response_json, required_only=True)
    log_request_response(url, response, headers, payload)
    created_inventories.append(response_json)


# TC-29 – Admin > Catalog > Inventory - Crear inventory con valor de prioridad 0.
@pytest.mark.functional
@pytest.mark.medium
def test_TC29_crear_inventory_con_prioridad_cero(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = create_inventory_data(priority=0)
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload, required_only=True)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    assert response_json["priority"] == 0
    log_request_response(url, response, headers, payload)
    created_inventories.append(response_json)


# TC-30 – Admin > Catalog > Inventory - Crear inventory con code duplicado.
@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC30_crear_inventory_con_code_duplicado(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload1 = create_inventory_data()
    url = EndpointInventory.inventory()
    response1 = SyliusRequest.post(url, headers, payload1)
    AssertionStatusCode.assert_status_code_201(response1)
    log_request_response(url, response1, headers, payload1)
    created_inventory = response1.json()
    created_inventories.append(created_inventory)
    payload2 = create_inventory_data(code=payload1["code"])
    response2 = SyliusRequest.post(url, headers, payload2)
    AssertionStatusCode.assert_status_code_422(response2)
    response_json = response2.json()
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 422, "code: Code has to be unique")


# TC-31 – Admin > Catalog > Inventory - Crear inventory sin campo code.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC31_crear_inventory_sin_campo_code(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = create_inventory_data()
    payload.pop("code")
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 422, "code: Code cannot be blank")
    log_request_response(url, response, headers, payload)


# TC-252 – Admin > Catalog > Inventory - Crear inventory sin campo name.
@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC252_crear_inventory_sin_campo_name(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = create_inventory_data()
    payload.pop("name")
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 422, "name: Name cannot be blank")
    log_request_response(url, response, headers, payload)


# TC-253 – Admin > Catalog > Inventory - Crear inventory con code como vacío ("").
@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC253_crear_inventory_con_code_vacio(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = create_inventory_data()
    payload["code"] = ""
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 422, "code: Code cannot be blank")
    log_request_response(url, response, headers, payload)


# TC-254 – Admin > Catalog > Inventory - Crear inventory con name como vacío ("").
@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC254_crear_inventory_con_name_vacio(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = create_inventory_data()
    payload["name"] = ""
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 422, "name: Name cannot be blank")
    log_request_response(url, response, headers, payload)


# TC-255 – Admin > Catalog > Inventory - Crear inventory con prioridad negativa.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.medium
@pytest.mark.xfail(reason="BUG255: Permite ingresar un valor negativo", run=True)
def test_TC255_crear_inventory_con_prioridad_negativa(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["priority"] = -5
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    response_json = response.json()
    created_inventories.append(response_json)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 422, "priority: Priority cannot be negative")


# TC-256 – Admin > Catalog > Inventory - Crear inventory con priority como texto.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC256_crear_inventory_con_priority_como_texto(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = create_inventory_data()
    payload["priority"] = "alta"
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 400, 'The type of the "priority" attribute must be "int", "string" given.')


# TC-257 – Admin > Catalog > Inventory - Crear inventory con priority como decimal.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.medium
def test_TC257_crear_inventory_con_priority_como_decimal(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = create_inventory_data()
    payload["priority"] = 3.14
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 400, 'The type of the "priority" attribute must be "int", "double" given.')


# TC-258 – Admin > Catalog > Inventory - Crear inventory con address válido.
@pytest.mark.functional
@pytest.mark.medium
def test_TC258_crear_inventory_con_address_valido(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    AssertionInventoryCreate.assert_inventory_response(payload, response_json)
    assert response_json["address"] is not None
    assert isinstance(response_json["address"], str)
    assert response_json["address"] != ""
    created_inventories.append(response_json)


# TC-259 – Admin > Catalog > Inventory - Crear inventory sin address.
@pytest.mark.functional
@pytest.mark.medium
def test_TC259_crear_inventory_sin_address(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    payload.pop("address")
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload, required_only=True)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    AssertionInventoryCreate.assert_inventory_response(payload, response_json)
    assert "address" in response_json
    assert response_json["address"] is None
    created_inventories.append(response_json)


# TC-260 – Admin > Catalog > Inventory - Crear inventory sin campo countryCode en address.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC260_crear_inventory_sin_country_code_en_address(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["address"].pop("countryCode")
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload, required_only=True)
    log_request_response(url, response, headers, payload)
    assert "countryCode" not in payload["address"]
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    assert response_json["address"] != ""
    created_inventories.append(response_json)


# TC-261 – Admin > Catalog > Inventory - Crear inventory con countryCode inválido.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC261_crear_inventory_con_country_code_invalido(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["address"]["countryCode"] = "XX"
    url = EndpointInventory.inventory()
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload, required_only=True)
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 422, 'address.countryCode: This value is not a valid country.')


# TC-262 – Admin > Catalog > Inventory - Crear inventory con estructura inválida de address.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC262_crear_inventory_con_address_invalido(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["address"] = "invalid"
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 400, 'Invalid IRI "invalid".')


# TC-263 – Admin > Catalog > Inventory - Crear inventory sin channels.
@pytest.mark.functional
@pytest.mark.medium
def test_TC263_crear_inventory_sin_channels(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    payload.pop("channels")
    url = EndpointInventory.inventory()
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload, required_only=True)
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    assert len(response_json["channels"]) == 0
    created_inventories.append(response_json)


# TC-264 – Admin > Catalog > Inventory - Crear inventory con channels inválido (formato incorrecto).
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC264_crear_inventory_con_channels_invalidos(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["channels"] = ["/api/v2/admin/channels/INVALID_CHANNEL"]
    url = EndpointInventory.inventory()
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload, required_only=True)
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    assert response_json["status"] == 400
    assert "Item not found for" in response_json["detail"]


# TC-265 – Admin > Catalog > Inventory - Crear inventory con código y nombre de longitud máxima válida.
@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.high
def test_TC265_crear_inventory_con_code_y_name_longitud_maxima(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = create_inventory_data(code="X" * 255, name="X" * 255)
    url = EndpointInventory.inventory()
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload, required_only=True)
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    AssertionInventoryCreate.assert_inventory_response(payload, response_json, required_only=True)
    created_inventories.append(response_json)


# TC-266 – Admin > Catalog > Inventory - Crear inventory con name extremadamente largo.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
@pytest.mark.xfail(reason="BUG266: El backend responde status=500 en lugar de validar longitud de 'name'", run=True)
def test_TC266_crear_inventory_con_name_extremadamente_largo(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = create_inventory_data(name="N" * 256)
    url = EndpointInventory.inventory()
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload, required_only=True)
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)


# TC-267 – Admin > Catalog > Inventory - Crear inventory con code extremadamente largo.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
@pytest.mark.xfail(reason="BUG266: El backend responde 500 en lugar de validar longitud de 'code'", run=True)
def test_TC267_crear_inventory_con_code_extremadamente_largo(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = create_inventory_data(code="C" * 256)
    url = EndpointInventory.inventory()
    AssertionInventory.assert_inventory_add_input_schema(payload)
    AssertionInventoryCreate.assert_inventory_payload(payload, required_only=True)
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)


# TC-268 – Admin > Catalog > Inventory - Crear inventory sin payload.
@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_TC268_crear_inventory_sin_payload(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = ""
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    AssertionInventoryErrors.assert_inventory_error_request(response_json, 400, 'Syntax error')