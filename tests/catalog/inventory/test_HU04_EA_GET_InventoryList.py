import pytest

from src.assertions.inventory_assertions import AssertionInventory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_inventory import EndpointInventory
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response

@pytest.mark.smoke
@pytest.mark.regression
def test_TC23_lista_completa_fuentes_inventarioo(auth_headers):
    url = EndpointInventory.inventory()
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionInventory.assert_inventory_list_schema(response.json())
    response_json = response.json()
    assert response_json["@context"].strip() != ""
    assert response_json["@id"].strip() != ""
    assert response_json["@type"].strip() != ""
    assert response_json["hydra:totalItems"] >= 0
    if response_json["hydra:member"]:
        item = response_json["hydra:member"][0]
        assert item["@id"].strip() != ""
        assert item["@type"].strip() != ""
        assert item["id"] > 0
        assert item["code"].strip() != ""
        assert item["name"].strip() != ""
        assert item["priority"] >= 0
        assert len(item["channels"]) > 0
        assert all(c.strip() != "" for c in item["channels"])
    log_request_response(url, response, auth_headers)

def test_TC25_fuente_inventario_por_id_existente(auth_headers):
    url = EndpointInventory.code("hamburg_warehouse")
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)

def test_TC24_fuente_inventario_id_inexistente(auth_headers):
    url = EndpointInventory.code("code_inexistente")
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)

def test_TC26_lista_sin_autenticacion():
    url = EndpointInventory.inventory()
    response = SyliusRequest.get(url, {})
    AssertionStatusCode.assert_status_code_401(response)

def test_TC206_fuente_sin_autenticacion():
    url = EndpointInventory.code("hamburg_warehouse")
    response = SyliusRequest.get(url, {})
    AssertionStatusCode.assert_status_code_401(response)

def test_TC207_lista_con_token_expirado(auth_headers):
    auth_headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.ey"
                       "JpYXQiOjE3NTQyMzQzODksImV4cCI6MTc1NDIzNzk4OSwicm9sZXMiOlsiUk9MRV"
                       "9BRE1JTklTVFJBVElPTl9BQ0NFU1MiLCJST0xFX0FQSV9BQ0NFU1MiXSwidXNlcm"
                       "5hbWUiOiJhcGkifQ.GmVMaimodyHNL8R9wToFg5RoOTwd9Rjf2WVqI_WoZJjAZJ1y"
                       "kbaBlsbC4TWwPqZuaEpPhFJlRotqezn0_HF7MumgZBK1rvmfX4M7QqQBeeohmZmt8"
                       "JB0eAjaqn-GtmmWeXrV1bCHxvqb-W1pbPsBQ1leKfnYeUnMPwrhPBsqdOAAEVK0ZWj"
                       "_LAbgYWlViEZ8uw7qxDR5gzmd6GwKEawLDlMa9Lj5Hz8sG7NuYonU-b38U_mOkN57x"
                       "r4SSL7DTkdk-q9rIOt-I056tzCKPR2Fx0CxCSO7MMP9pVN9sHMz53srPpHTvwtRCZS"
                       "gzRB4PGU6mzsmfl4l7sLE72OouL-y_eVqgKJ-7YG5D_ZNp8vgaALqYDzbAySDb_ktF"
                       "tCCWzhMxasoBOLoCzy3J1URprwxyPcYabntVyr8O42mkIjh1iGH-IASK9M614epkcB"
                       "cSIbyB5cwkTwfBCAhMwqot6Ec6ozT8VKmfYAZdtisKpVarQrs25CRzdT1kZrRr57Fs"
                       "GgLQgf05K39QLM5wvjEd2i7NiRwCPVeqFVzJgBKN0DQBLK3a7zoN3a_mV7KCGmxoTk"
                       "0RfYEhv00EpxVjMUWg40Cpg22YlFD1WZNxrN1r4Wt0LqkZfCfwPzD9Ci2X45oDjzPm"
                       "Iu6goaWDaaSgpaIeB6pxy-AuWi3ofhXlZkvlTgEm0"}
    url = EndpointInventory.inventory()
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_401(response)

def test_TC208_fuente_con_token_expirado(auth_headers):
    auth_headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.ey"
                       "JpYXQiOjE3NTQyMzQzODksImV4cCI6MTc1NDIzNzk4OSwicm9sZXMiOlsiUk9MRV"
                       "9BRE1JTklTVFJBVElPTl9BQ0NFU1MiLCJST0xFX0FQSV9BQ0NFU1MiXSwidXNlcm"
                       "5hbWUiOiJhcGkifQ.GmVMaimodyHNL8R9wToFg5RoOTwd9Rjf2WVqI_WoZJjAZJ1y"
                       "kbaBlsbC4TWwPqZuaEpPhFJlRotqezn0_HF7MumgZBK1rvmfX4M7QqQBeeohmZmt8"
                       "JB0eAjaqn-GtmmWeXrV1bCHxvqb-W1pbPsBQ1leKfnYeUnMPwrhPBsqdOAAEVK0ZWj"
                       "_LAbgYWlViEZ8uw7qxDR5gzmd6GwKEawLDlMa9Lj5Hz8sG7NuYonU-b38U_mOkN57x"
                       "r4SSL7DTkdk-q9rIOt-I056tzCKPR2Fx0CxCSO7MMP9pVN9sHMz53srPpHTvwtRCZS"
                       "gzRB4PGU6mzsmfl4l7sLE72OouL-y_eVqgKJ-7YG5D_ZNp8vgaALqYDzbAySDb_ktF"
                       "tCCWzhMxasoBOLoCzy3J1URprwxyPcYabntVyr8O42mkIjh1iGH-IASK9M614epkcB"
                       "cSIbyB5cwkTwfBCAhMwqot6Ec6ozT8VKmfYAZdtisKpVarQrs25CRzdT1kZrRr57Fs"
                       "GgLQgf05K39QLM5wvjEd2i7NiRwCPVeqFVzJgBKN0DQBLK3a7zoN3a_mV7KCGmxoTk"
                       "0RfYEhv00EpxVjMUWg40Cpg22YlFD1WZNxrN1r4Wt0LqkZfCfwPzD9Ci2X45oDjzPm"
                       "Iu6goaWDaaSgpaIeB6pxy-AuWi3ofhXlZkvlTgEm0"}
    url = EndpointInventory.code('hamburg_warehouse')
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_401(response)

def test_TC209_pagina_valida_y_items_validos(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)

def test_TC210_pagina_igual_cero_items_validos(auth_headers):
    params = {
        'page': 0,
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)

def test_TC211_pagina_negativa_items_validos(auth_headers):
    params = {
        'page': -1,
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.xfail(reason="Knwon issue BUG001: Rompe la URL", run=False)
def test_TC212_pagina_decimal_items_validos(auth_headers):
    params = {
        'page': -1,
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)

def test_TC213_pagina_string_items_validos(auth_headers):
    params = {
        'page': "uno",
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)

def test_TC214_pagina_vacia_items_validos(auth_headers):
    params = {
        'page': '',
        'itemsPerPage': 1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.xfail(reason="Knwon issue BUG002: Rompe la URL", run=False)
def test_TC215_items_igual_cero_pagina_valida(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': 0
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)

def test_TC216_items_negativo_pagina_valida(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': -1
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.xfail(reason="Knwon issue BUG003: Rompe la URL", run=False)
def test_TC217_items_decimal_pagina_valida(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': 1.5
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.xfail(reason="Knwon issue BUG004: Rompe la URL", run=False)
def test_TC218_items_string_pagina_valida(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': "uno"
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(url, response, auth_headers)

@pytest.mark.xfail(reason="Knwon issue BUG005: Rompe la URL", run=False)
def test_TC219_items_vacio_pagina_valida(auth_headers):
    params = {
        'page': 1,
        'itemsPerPage': ''
    }
    url = EndpointInventory.inventory_with_params(**params)
    response = SyliusRequest.get(url, auth_headers)
    log_request_response(url, response, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    #pytest.fail("[BUG001]")