import pytest

from src.assertions.inventory_assertions.inventory_schema_assertions import AssertionInventory
from src.assertions.inventory_assertions.inventory_get_content_assertions import AssertionInventoryFields
from src.assertions.inventory_assertions.inventory_errors_assertions import AssertionInventoryErrors
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_inventory import EndpointInventory
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response

@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.regression
def test_TC23_lista_completa_fuentes_inventario(setup_teardown_view_inventory):
    headers, _, _ = setup_teardown_view_inventory
    url = EndpointInventory.inventory()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_list_schema(response_json)
    AssertionInventoryFields.assert_inventory_root_metadata(response_json)
    log_request_response(url, response, headers)


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.regression
def test_TC25_fuente_inventario_por_code_existente(setup_teardown_view_inventory):
    headers, inventory1, _ = setup_teardown_view_inventory
    code = inventory1['code']
    url = EndpointInventory.code(code)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionInventory.assert_inventory_code_schema(response_json)
    AssertionInventoryFields.assert_inventory_item_content(response_json, code)
    log_request_response(url, response, headers)


@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
def test_TC24_fuente_inventario_code_inexistente(setup_teardown_view_inventory):
    headers, _, _ = setup_teardown_view_inventory
    code = "code_inexistente"
    url = EndpointInventory.code(code)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionInventoryErrors.assert_inventory_error_request(response.json(), 404, "Not Found")
    log_request_response(url, response, headers)


@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
def test_TC26_lista_sin_autenticacion():
    url = EndpointInventory.inventory()
    response = SyliusRequest.get(url, {})
    AssertionStatusCode.assert_status_code_401(response)
    AssertionInventoryErrors.assert_inventory_errors(response.json(), 401, "JWT Token not found")
    log_request_response(url, response)


@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
def test_TC206_fuente_sin_autenticacion():
    url = EndpointInventory.code("hamburg_warehouse")
    response = SyliusRequest.get(url, {})
    AssertionStatusCode.assert_status_code_401(response)
    AssertionInventoryErrors.assert_inventory_errors(response.json(), 401, "JWT Token not found")
    log_request_response(url, response)


@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
def test_TC207_lista_con_token_expirado(setup_teardown_view_inventory):
    headers, _, _ = setup_teardown_view_inventory
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTQzNjg3MTcsImV4cCI6MTc1NDM3MjMxNywicm9sZXMiOlsiUk9MRV9BRE1JTklTVFJBVElPTl9BQ0NFU1MiLCJST0xFX0FQSV9BQ0NFU1MiXSwidXNlcm5hbWUiOiJhcGkifQ.kCQgpWu-6UHG0hPiMacehDGUWBVf3L6R9MEkwujopo-lo6GkwEtXndnWgCyyzPQcZmoMuMAocDRT5NVaR1tU_YYPLi-haJ9dYuWe7-2vPz6wgPeOfuXWGnIbNKd-nrOZtLz8naX5xYRQAZdvkSVN6-tVfPHyKtQwcI-gii2mW1qQO2TwfVVQBHEwrrsRxuqKbkah4nPmICP4na8hM3svn2oYJA96knq6rfWcCEyCVAm3gRpyoFG-iyaYSJMPeRZvYa0Ua4HuWDaXnIYGGbAUuGOlyGpfOq5s1pAdSBSUPsOEYWRczQsCHwi6IEnKO9hNyNgKMfjW7B5ba3vmT6IZERhM_hjfNHW9s83Um0kLiMyMhkGW6PmsOTZdoIsyscUO1uhj6mHXi9fJ53lgyxIkbQSRadczj7cxCnHPtBrpCdiQrQgF8JW3wZJHe_GIDtWB67_0lf8Fs60ntPzIB2pVJIohC95OoqSzoVvLcKae9pGfmPJz0JLevtA9xXUwSkK8v9ixVEWSyJt89j8XVkZ6dqEFAR1qOAk9Uh9AZN9c3ImkLF7XHmlHHoJsFLuwpjEoGS5m4Ul7V0InPVHAI-ys_JVL3hPpVLBxlTr66l8j2wPTnCozNYS7w5-w-0pLtDy4ajMYjU2ICpci1VbJsCP-kzIrdIg2nz5PuO33v9SDyZg"}
    url = EndpointInventory.inventory()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionInventoryErrors.assert_inventory_errors(response.json(), 401, "Expired JWT Token")
    log_request_response(url, response, headers)


@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
def test_TC208_fuente_con_token_expirado(setup_teardown_view_inventory):
    headers, _, _ = setup_teardown_view_inventory
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTQzNjg3MTcsImV4cCI6MTc1NDM3MjMxNywicm9sZXMiOlsiUk9MRV9BRE1JTklTVFJBVElPTl9BQ0NFU1MiLCJST0xFX0FQSV9BQ0NFU1MiXSwidXNlcm5hbWUiOiJhcGkifQ.kCQgpWu-6UHG0hPiMacehDGUWBVf3L6R9MEkwujopo-lo6GkwEtXndnWgCyyzPQcZmoMuMAocDRT5NVaR1tU_YYPLi-haJ9dYuWe7-2vPz6wgPeOfuXWGnIbNKd-nrOZtLz8naX5xYRQAZdvkSVN6-tVfPHyKtQwcI-gii2mW1qQO2TwfVVQBHEwrrsRxuqKbkah4nPmICP4na8hM3svn2oYJA96knq6rfWcCEyCVAm3gRpyoFG-iyaYSJMPeRZvYa0Ua4HuWDaXnIYGGbAUuGOlyGpfOq5s1pAdSBSUPsOEYWRczQsCHwi6IEnKO9hNyNgKMfjW7B5ba3vmT6IZERhM_hjfNHW9s83Um0kLiMyMhkGW6PmsOTZdoIsyscUO1uhj6mHXi9fJ53lgyxIkbQSRadczj7cxCnHPtBrpCdiQrQgF8JW3wZJHe_GIDtWB67_0lf8Fs60ntPzIB2pVJIohC95OoqSzoVvLcKae9pGfmPJz0JLevtA9xXUwSkK8v9ixVEWSyJt89j8XVkZ6dqEFAR1qOAk9Uh9AZN9c3ImkLF7XHmlHHoJsFLuwpjEoGS5m4Ul7V0InPVHAI-ys_JVL3hPpVLBxlTr66l8j2wPTnCozNYS7w5-w-0pLtDy4ajMYjU2ICpci1VbJsCP-kzIrdIg2nz5PuO33v9SDyZg"}
    url = EndpointInventory.code('hamburg_warehouse')
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionInventoryErrors.assert_inventory_errors(response.json(), 401, "Expired JWT Token")
    log_request_response(url, response)


@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.security
@pytest.mark.parametrize("page, itemsPerPage", [
    (None, 1),
    (None, 0),
    (1, None),
    (1, 1),
    (1, 0),
    (2, 1)
])
def test_209_215_pagina_e_items_validas(setup_teardown_view_inventory, page, itemsPerPage):
    headers, _, _ = setup_teardown_view_inventory
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, headers)
    log_request_response(url, response, headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionInventoryFields.assert_inventory_root_metadata(response.json(), params=params)


@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
@pytest.mark.parametrize("page, itemsPerPage", [
    (0, 1),
    (-1, 1),
    pytest.param(1.5, 1, marks=pytest.mark.xfail(reason="BUG212: El parámetro page acepta decimales y rompe la URL", run=True)),
    ("uno", 1),
    ('', 1),
    (1, -1),
    pytest.param(1, 1.5, marks=pytest.mark.xfail(reason="BUG217: El param itemsPerPage puede ser decimal rompiendo la URL", run=True)),
    pytest.param(1, "uno", marks=pytest.mark.xfail(reason="BUG218: El param itemsPerPage puede ser string rompiendo la URL", run=True)),
    pytest.param(1, '', marks=pytest.mark.xfail(reason="BUG219: El param itemsPerPage puede ser vacio rompiendo la URL", run=True))
])
def test_210_219_pagina_e_items_invalidas(setup_teardown_view_inventory, page, itemsPerPage):
    headers, _, _ = setup_teardown_view_inventory
    params = {"page": page, "itemsPerPage": itemsPerPage}
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, headers)
    log_request_response(url, response, headers)
    AssertionStatusCode.assert_status_code_400(response)


"""
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.security
def test_TC209_pagina_valida_y_items_validos(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    assert len(response_json["hydra:member"]) == params["itemsPerPage"]
    expected_id = f"/api/v2/admin/inventory-sources?itemsPerPage={params['itemsPerPage']}&page={params['page']}"
    assert response_json["hydra:view"]["@id"] == expected_id
    log_request_response(url, response, auth_headers)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
def test_TC210_pagina_igual_cero_items_validos(auth_headers):
    params = {'page': 0, 'itemsPerPage': 1}
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    AssertionInventoryErrors.assert_inventory_error_request(response.json(), 400, "Page should not be less than 1")
    log_request_response(url, response, auth_headers)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
def test_TC211_pagina_negativa_items_validos(auth_headers):
    params = {
        'page': -1,
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    assert response_json["@type"] == "hydra:Error"
    assert response_json["detail"] == "Page should not be less than 1"
    assert response_json["status"] == 400
    log_request_response(url, response, auth_headers)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
@pytest.mark.xfail(reason="Knwon issue BUG212: El param page puede ser decimal rompiendo la URL", run=True)
def test_TC212_pagina_decimal_items_validos(auth_headers):
    params = {
        'page': 1.5,
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
def test_TC213_pagina_string_items_validos(auth_headers):
    params = {
        'page': "uno",
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    assert response_json["@type"] == "hydra:Error"
    assert response_json["detail"] == "Page should not be less than 1"
    assert response_json["status"] == 400
    log_request_response(url, response, auth_headers)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
def test_TC214_pagina_vacia_items_validos(auth_headers):
    params = {
        'page': '',
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    assert response_json["@type"] == "hydra:Error"
    assert response_json["detail"] == "Page should not be less than 1"
    assert response_json["status"] == 400
    log_request_response(url, response, auth_headers)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
def test_TC215_items_igual_cero_pagina_valida(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': 0
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    assert len(response_json["hydra:member"]) == params["itemsPerPage"]
    expected_id = f"/api/v2/admin/inventory-sources?itemsPerPage={params['itemsPerPage']}"
    assert response_json["hydra:view"]["@id"] == expected_id
    log_request_response(url, response, auth_headers)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
def test_TC216_items_negativo_pagina_valida(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': -1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    assert response_json["@type"] == "hydra:Error"
    assert response_json["detail"] == "Limit should not be less than 0"
    assert response_json["status"] == 400
    log_request_response(url, response, auth_headers)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
@pytest.mark.xfail(reason="Knwon issue BUG217: El param itemsPerPage puede ser decimal rompiendo la URL", run=True)
def test_TC217_items_decimal_pagina_valida(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': 1.5
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(url, response, auth_headers)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
@pytest.mark.xfail(reason="Knwon issue BUG218: El param itemsPerPage puede ser string rompiendo la URL", run=True)
def test_TC218_items_string_pagina_valida(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': "uno"
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(url, response, auth_headers)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.security
@pytest.mark.xfail(reason="Knwon issue BUG219: El param itemsPerPage puede ser vacio rompiendo la URL", run=True)
def test_TC219_items_vacio_pagina_valida(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': ''
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    log_request_response(url, response, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)

"""