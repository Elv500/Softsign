import pytest

from src.routes.request import SyliusRequest
from src.routes.endpoint_inventory import EndpointInventory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.assertions.inventory_assertions.inventory_schema_assertions import AssertionInventory
from src.assertions.inventory_assertions.inventory_errors_assertions import AssertionInventoryErrors
from src.data.inventory import generate_inventory_source_data, create_inventory_data
from utils.logger_helpers import log_request_response

def test_TC69_actualizacion_completa_campos_validos(setup_edit_inventory):
    headers, inventory = setup_edit_inventory
    url = EndpointInventory.code(inventory["code"])
    responseBefore = SyliusRequest.get(url, headers)
    AssertionInventory.assert_inventory_code_schema(responseBefore.json())
    log_request_response(url, responseBefore)
    payload = generate_inventory_source_data()
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    AssertionInventory.assert_inventory_edit_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionInventory.assert_inventory_code_schema(response.json())
    log_request_response(url, response, headers, payload)


def test_TC70_actualizacion_solo_campos_obligatorios_name(setup_edit_inventory):
    headers, inventory = setup_edit_inventory
    url = EndpointInventory.code(inventory["code"])
    responseBefore = SyliusRequest.get(url, headers)
    AssertionInventory.assert_inventory_code_schema(responseBefore.json())
    log_request_response(url, responseBefore)
    payload = generate_inventory_source_data(required_only=True)
    response = SyliusRequest.put(url, headers, payload)
    AssertionInventory.assert_inventory_edit_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionInventory.assert_inventory_code_schema(response.json())
    log_request_response(url, response, headers, payload)


def test_TC71_actualizacion_campo_opcional_channels_vacio(setup_edit_inventory):
    headers, inventory = setup_edit_inventory
    url = EndpointInventory.code(inventory["code"])
    responseBefore = SyliusRequest.get(url, headers)
    AssertionInventory.assert_inventory_code_schema(responseBefore.json())
    log_request_response(url, responseBefore)
    payload = generate_inventory_source_data()
    payload.pop("channels")
    response = SyliusRequest.put(url, headers, payload)
    AssertionInventory.assert_inventory_edit_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionInventory.assert_inventory_code_schema(response.json())
    log_request_response(url, response, headers, payload)


def test_TC72_actualizacion_sin_campo_name(setup_edit_inventory):
    headers, inventory = setup_edit_inventory
    url = EndpointInventory.code(inventory["code"])
    responseBefore = SyliusRequest.get(url, headers)
    AssertionInventory.assert_inventory_code_schema(responseBefore.json())
    log_request_response(url, responseBefore)
    payload = generate_inventory_source_data()
    payload.pop("name")
    response = SyliusRequest.put(url, headers, payload)
    AssertionInventory.assert_inventory_edit_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionInventory.assert_inventory_code_schema(response.json())
    log_request_response(url, response, headers, payload)


@pytest.mark.xfail(reason="BUG73: Permite ingresar un valor negativo", run=True)
def test_TC73_actualizacion_formato_invalido_priority(setup_edit_inventory):
    headers, inventory = setup_edit_inventory
    url = EndpointInventory.code(inventory["code"])
    responseBefore = SyliusRequest.get(url, headers)
    AssertionInventory.assert_inventory_code_schema(responseBefore.json())
    log_request_response(url, responseBefore)
    payload = generate_inventory_source_data()
    payload["priority"] = -1
    response = SyliusRequest.put(url, headers, payload)
    AssertionInventory.assert_inventory_edit_input_schema(payload)
    AssertionStatusCode.assert_status_code_400(response)
    AssertionInventory.assert_inventory_code_schema(response.json())
    log_request_response(url, response, headers, payload)


def test_TC331_actualizacion_inventario_inexistente(setup_edit_inventory):
    headers, inventory = setup_edit_inventory
    url = EndpointInventory.code(f'{inventory["code"]}x')
    payload = generate_inventory_source_data()
    response = SyliusRequest.put(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionInventoryErrors.assert_inventory_error_request(response.json(), 404, "Not Found")
    

def test_TC332_actualizacion_sin_token_autenticacion(setup_edit_inventory):
    headers, inventory = setup_edit_inventory
    url = EndpointInventory.code(inventory["code"])
    payload = generate_inventory_source_data()
    response = SyliusRequest.put(url, headers={}, payload=payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionInventoryErrors.assert_inventory_errors(response.json(), 401, "JWT Token not found")


def test_TC333_actualizacion_usuario_sin_permisos(setup_edit_inventory):
    headers, inventory = setup_edit_inventory
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTQzNjg3MTcsImV4cCI6MTc1NDM3MjMxNywicm9sZXMiOlsiUk9MRV9BRE1JTklTVFJBVElPTl9BQ0NFU1MiLCJST0xFX0FQSV9BQ0NFU1MiXSwidXNlcm5hbWUiOiJhcGkifQ.kCQgpWu-6UHG0hPiMacehDGUWBVf3L6R9MEkwujopo-lo6GkwEtXndnWgCyyzPQcZmoMuMAocDRT5NVaR1tU_YYPLi-haJ9dYuWe7-2vPz6wgPeOfuXWGnIbNKd-nrOZtLz8naX5xYRQAZdvkSVN6-tVfPHyKtQwcI-gii2mW1qQO2TwfVVQBHEwrrsRxuqKbkah4nPmICP4na8hM3svn2oYJA96knq6rfWcCEyCVAm3gRpyoFG-iyaYSJMPeRZvYa0Ua4HuWDaXnIYGGbAUuGOlyGpfOq5s1pAdSBSUPsOEYWRczQsCHwi6IEnKO9hNyNgKMfjW7B5ba3vmT6IZERhM_hjfNHW9s83Um0kLiMyMhkGW6PmsOTZdoIsyscUO1uhj6mHXi9fJ53lgyxIkbQSRadczj7cxCnHPtBrpCdiQrQgF8JW3wZJHe_GIDtWB67_0lf8Fs60ntPzIB2pVJIohC95OoqSzoVvLcKae9pGfmPJz0JLevtA9xXUwSkK8v9ixVEWSyJt89j8XVkZ6dqEFAR1qOAk9Uh9AZN9c3ImkLF7XHmlHHoJsFLuwpjEoGS5m4Ul7V0InPVHAI-ys_JVL3hPpVLBxlTr66l8j2wPTnCozNYS7w5-w-0pLtDy4ajMYjU2ICpci1VbJsCP-kzIrdIg2nz5PuO33v9SDyZg"}
    url = EndpointInventory.code(inventory["code"])
    payload = generate_inventory_source_data()
    response = SyliusRequest.put(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionInventoryErrors.assert_inventory_errors(response.json(), 401, "Expired JWT Token")


def test_TC335_intento_actualizar_code_insatisfactoriamente(setup_edit_inventory):
    headers, inventory = setup_edit_inventory
    url = EndpointInventory.code(inventory["code"])
    responseBefore = SyliusRequest.get(url, headers)
    AssertionInventory.assert_inventory_code_schema(responseBefore.json())
    log_request_response(url, responseBefore)
    payload = generate_inventory_source_data()
    response = SyliusRequest.put(url, headers, payload)
    AssertionInventory.assert_inventory_edit_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionInventory.assert_inventory_code_schema(response.json())
    log_request_response(url, response, headers, payload)

@pytest.mark.xfail(reason="BUG336: Permite actualizar con campos faltantes como si fuera patch", run=True)
def test_TC336_actualizacion_un_campo_priority_verificar_borrado_campos(setup_edit_inventory):
    headers, inventory = setup_edit_inventory
    url = EndpointInventory.code(inventory["code"])
    responseBefore = SyliusRequest.get(url, headers)
    AssertionInventory.assert_inventory_code_schema(responseBefore.json())
    log_request_response(url, responseBefore)
    payload = create_inventory_data(priority=2)
    response = SyliusRequest.put(url, headers, payload)
    AssertionInventory.assert_inventory_edit_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionInventory.assert_inventory_code_schema(response.json())
    log_request_response(url, response, headers, payload)
    assert inventory["address"] == {}
    assert inventory["channels"] == []