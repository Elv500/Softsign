import pytest

from src.assertions.inventory_assertions import AssertionInventory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_inventory import EndpointInventory
from src.routes.request import SyliusRequest
from src.data.inventory import generate_inventory_source_data
from utils.logger_helpers import log_request_response

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.functional
def test_TC27_crear_inventory_con_todos_los_campos_validos(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionInventory.assert_inventory_add_input_schema(payload)
    assert all(campo.strip() != "" for campo in payload["address"].values())
    assert payload["code"] != ""
    assert payload["name"] != ""
    assert payload["priority"] >= 0
    assert len(payload["channels"]) >= 0
    assert all(channel.strip() != "" for channel in payload["channels"])
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    #assert response_json["address"] == payload["address"]
    assert response_json["id"] >= 0
    assert response_json["code"] == payload["code"]
    assert response_json["name"] == payload["name"]
    assert response_json["priority"] == payload["priority"]
    assert response_json["channels"] == payload["channels"]
    log_request_response(url, response, headers, payload)
    created_inventories.append(response_json)

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.functional
def test_TC28_crear_inventory_con_campos_requeridos(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data(required_only=True)
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionInventory.assert_inventory_add_input_schema(payload)
    assert payload["code"] != ""
    assert payload["name"] != ""
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    assert response_json["id"] >= 0
    assert response_json["code"] == payload["code"]
    assert response_json["name"] == payload["name"]
    log_request_response(url, response, headers, payload)
    created_inventories.append(response_json)

@pytest.mark.regression
@pytest.mark.functional
def test_TC29_crear_inventory_con_prioridad_cero(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["priority"] = 0
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionInventory.assert_inventory_add_input_schema(payload)
    assert payload["priority"] == 0
    assert payload["code"] != ""
    assert payload["name"] != ""
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    assert response_json["priority"] == 0
    log_request_response(url, response, headers, payload)
    created_inventories.append(response_json)

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
def test_TC30_crear_inventory_con_code_duplicado(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload1 = generate_inventory_source_data()
    url = EndpointInventory.inventory()
    response1 = SyliusRequest.post(url, headers, payload1)
    AssertionStatusCode.assert_status_code_201(response1)
    created_inventory = response1.json()
    created_inventories.append(created_inventory)
    payload2 = generate_inventory_source_data()
    payload2["code"] = payload1["code"]
    response2 = SyliusRequest.post(url, headers, payload2)
    AssertionStatusCode.assert_status_code_422(response2)
    response_json = response2.json()
    assert response_json["status"] == 422
    assert response_json["detail"] == "code: Code has to be unique"
    log_request_response(url, response2, headers, payload2)

@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
def test_TC31_crear_inventory_sin_campo_code(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload.pop("code")
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    assert response_json["status"] == 422
    assert response_json["detail"] == "code: Code cannot be blank" 
    log_request_response(url, response, headers, payload)

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
def test_TC252_crear_inventory_sin_campo_name(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload.pop("name")
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    assert response_json["status"] == 422
    assert response_json["detail"] == "name: Name cannot be blank"
    log_request_response(url, response, headers, payload)

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
def test_TC253_crear_inventory_con_code_vacio(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["code"] = ""
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    assert response_json["status"] == 422
    assert response_json["detail"] == "code: Code cannot be blank"
    log_request_response(url, response, headers, payload)

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
def test_TC254_crear_inventory_con_name_vacio(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["name"] = ""
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    assert response_json["status"] == 422
    assert response_json["detail"] == "name: Name cannot be blank"
    log_request_response(url, response, headers, payload)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.xfail(reason="Knwon issue BUG01: Permite ingresar un valor negativo", run=True)
def test_TC255_crear_inventory_con_prioridad_negativa(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["priority"] = -5
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    assert response_json["status"] == 422
    assert response_json["detail"] == "priority: Priority cannot be negative"
    
@pytest.mark.functional
@pytest.mark.negative
def test_TC256_crear_inventory_con_priority_como_texto(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["priority"] = "alta"
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    assert response_json["status"] == 400
    assert response_json["detail"] == 'The type of the "priority" attribute must be "int", "string" given.'

@pytest.mark.functional
@pytest.mark.negative
def test_TC257_crear_inventory_con_priority_como_decimal(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["priority"] = 3.14
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    assert response_json["status"] == 400
    assert response_json["detail"] == 'The type of the "priority" attribute must be "int", "double" given.'

@pytest.mark.regression
@pytest.mark.functional
def test_TC258_crear_inventory_con_address_valido(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    assert response_json["code"] == payload["code"]
    assert response_json["name"] == payload["name"]
    assert response_json["priority"] == payload["priority"]
    assert response_json["channels"] == payload["channels"]
    assert response_json["address"] is not None
    assert isinstance(response_json["address"], str)
    assert response_json["address"] != ""
    created_inventories.append(response_json)

@pytest.mark.regression
@pytest.mark.functional
def test_TC259_crear_inventory_sin_address(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    payload.pop("address")
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    assert "address" in response_json
    assert response_json["address"] is None
    created_inventories.append(response_json)

@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
def test_TC260_crear_inventory_sin_country_code_en_address(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["address"].pop("countryCode")
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    assert "countryCode" not in payload["address"]
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    assert response_json["address"] != ""
    created_inventories.append(response_json)

@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
def test_TC261_crear_inventory_con_country_code_invalido(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["address"]["countryCode"] = "XX"
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    assert response_json["status"] == 422
    assert response_json["detail"] == 'address.countryCode: This value is not a valid country.'

@pytest.mark.functional
@pytest.mark.negative
def test_TC262_crear_inventory_con_address_invalido(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["address"] = "invalid"
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    assert response_json["status"] == 400
    assert response_json["detail"] == 'Invalid IRI "invalid".'

@pytest.mark.regression
@pytest.mark.functional
def test_TC263_crear_inventory_sin_channels(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    payload.pop("channels")
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    assert len(response_json["channels"]) == 0
    created_inventories.append(response_json)

@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
def test_TC264_crear_inventory_con_channels_invalidos(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["channels"] = ["/api/v2/admin/channels/INVALID_CHANNEL"]
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    assert response_json["status"] == 400
    assert "Item not found for" in response_json["detail"]

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.functional
def test_TC265_crear_inventory_con_code_y_name_longitud_maxima(setup_add_inventory):
    headers, created_inventories = setup_add_inventory
    payload = generate_inventory_source_data()
    max_length_value = "X" * 255
    payload["code"] = max_length_value
    payload["name"] = max_length_value
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_add_output_schema(response_json)
    assert response_json["code"] == max_length_value
    assert response_json["name"] == max_length_value
    created_inventories.append(response_json)

@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.xfail(reason="Knwon issue BUG01: El backend responde 500 en lugar de validar longitud de 'name'", run=True)
def test_TC266_crear_inventory_con_name_extremadamente_largo(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["name"] = "N" * 256
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)

@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.xfail(reason="Knwon issue BUG01: El backend responde 500 en lugar de validar longitud de 'code'", run=True)
def test_TC267_crear_inventory_con_code_extremadamente_largo(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = generate_inventory_source_data()
    payload["code"] = "C" * 256
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.negative
def test_TC268_crear_inventory_sin_payload(setup_add_inventory):
    headers, _ = setup_add_inventory
    payload = ""
    url = EndpointInventory.inventory()
    response = SyliusRequest.post(url, headers)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    assert response_json["status"] == 400
    assert response_json["detail"] == 'Syntax error'