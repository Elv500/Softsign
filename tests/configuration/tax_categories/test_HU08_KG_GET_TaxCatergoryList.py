import requests
import pytest
from utils.logger_helpers import log_request_response

from src.assertions.taxCategory_assertions import AssertionTaxCategory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_tax_category import EndpointTaxCategory
from src.routes.request import SyliusRequest

@pytest.mark.smoke
@pytest.mark.regression
def test_TC36_Ver_listado_de_categorías_de_impuestos_exitosamente(auth_headers):
    url= EndpointTaxCategory.tax_category()
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxCategory.assert_tax_category_list_schema(response.json())
    log_request_response(url, response, auth_headers)


@pytest.mark.functional
@pytest.mark.smoke
def test_TC37_verificar_codigo_respuesta_200_OK(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    response = requests.get(url, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.content, "La respuesta está vacía"



@pytest.mark.functional
@pytest.mark.smoke
def test_TC38_verificar_formato_jsonld(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    response = requests.get(url, headers=auth_headers)
    content_type = response.headers.get("Content-Type", "")
    assert "application/ld+json" in content_type, f"Se esperaba 'application/ld+json' en Content-Type, pero fue: {content_type}"


@pytest.mark.functional
@pytest.mark.smoke
def test_TC39_verificar_estructura_json(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    response = requests.get(url, headers=auth_headers)
    data = response.json()
    assert "hydra:member" in data, "'hydra:member' no está en la respuesta"
    for item in data["hydra:member"]:
        assert "code" in item, "Falta campo 'code'"
        assert "name" in item, "Falta campo 'name'"
        assert "description" in item, "Falta campo 'description'"



@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC40_verificar_errores_500_503_con_solicitud_valida(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code not in [500, 503], f"Se recibió error inesperado {response.status_code}"


@pytest.mark.functional
@pytest.mark.smoke
def test_TC41_verificar_error_parametros_invalidos(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    params = {
        "itemsPerPage": -1,
        "page": "abc"
    }
    response = requests.get(url, headers=auth_headers, params=params)
    assert response.status_code in [400, 422], f"Se esperaba error 400 o 422 pero se recibió {response.status_code}"


@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC42_verificar_respuesta_token_invalido_o_sin_autenticacion():
    url = f"{BASE_URL}/admin/tax-categories"
    response = requests.get(url)  # Sin headers
    assert response.status_code in [401, 403], f"Se esperaba 401 o 403, pero se recibió {response.status_code}"
