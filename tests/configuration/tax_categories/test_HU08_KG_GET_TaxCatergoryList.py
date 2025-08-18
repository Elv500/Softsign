import pytest
import logging
import requests

from src.assertions.TaxCategory_assertions.tax_category_get_content_assertions import AssertionTaxCategoryFields
from src.assertions.TaxCategory_assertions.tax_category_errors_assertions import AssertionTaxCategoryErrors
from src.assertions.TaxCategory_assertions.taxCategory_schema_assertions import AssertionTaxCategory
from src.resources.call_request.taxCategory_call import TaxCategoryCall
from src.data.taxCategory import generate_tax_category_data
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_tax_category import EndpointTaxCategory
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response



#TC_234: Iniciando test - Obtener listado de categoria del endpoit get
@pytest.mark.high
@pytest.mark.smoke
@pytest.mark.functional
def test_TC234_Ver_listado_de_categorías_de_impuestos_exitosamente(setup_teardown_view_tax_category):
    headers, _, _ = setup_teardown_view_tax_category
    url = EndpointTaxCategory.tax_category()
    response = SyliusRequest().get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxCategory.assert_tax_category_list_schema(response_json)
    AssertionTaxCategoryFields.assert_tax_category_root_metadata(response_json)
    log_request_response(url, response, headers)


#C_235: Iniciando test - verificar el codigo de respuesta 200ok al hacer una peticion
@pytest.mark.high
@pytest.mark.functional
@pytest.mark.smoke
def test_TC235_verificar_codigo_respuesta_200_OK(auth_headers):
    url = EndpointTaxCategory.tax_category()
    response = SyliusRequest.get(url, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    log_request_response(url, response, auth_headers)


#TC_237: Iniciando test - verficando la salida del edpoint tenga el formato json
@pytest.mark.medium
@pytest.mark.functional
@pytest.mark.smoke
def test_TC237_verificar_formato_jsonld(setup_teardown_view_tax_category,auth_headers):
    headers, tax_categories1, tax_categories2 = setup_teardown_view_tax_category
    url = EndpointTaxCategory.tax_category()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    content_type = response. headers.get("Content-Type", "")
    assert "application/ld+json" in content_type, (
        f"Content-Type debe ser 'application/ld+json'. Actual: {content_type}\n"
        f"Respuesta completa: {response.text}"
    )
    try:
        data = response.json()
    except ValueError as e:
        pytest.fail(f"La respuesta no es JSON válido: {str(e)}")
    log_request_response(url, response, auth_headers)


#TC_241: Iniciando test Validando la paginacion basica
@pytest.mark.medium
@pytest.mark.functional
@pytest.mark.regression
def test_TC241_validar_paginacion_basica_tax_category(auth_headers):
    url = EndpointTaxCategory.tax_category()
    response = SyliusRequest.get(EndpointTaxCategory.tax_category_with_params(page=1, itemsPerPage=2), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    data = response.json()
    assert isinstance(data.get("hydra:member", []), list)
    assert len(data["hydra:member"]) <= 2
    log_request_response(url, response, auth_headers)


#TC_236: Iniciando test - Validar que se puede obtener una categoría de impuesto filtrando por código
@pytest.mark.high
@pytest.mark.functional
@pytest.mark.smoke
def test_TC236_obtener_categoria_por_codigo(setup_add_tax_category, auth_headers):
    auth_headers, create_tax_category = setup_add_tax_category
    data = generate_tax_category_data()
    create_response = TaxCategoryCall.create(auth_headers, data)
    status_code = AssertionStatusCode.assert_status_code_201(create_response)
    created_category = create_response.json()
    create_tax_category.append(created_category)
    target_code = created_category["code"]
    url = f"{EndpointTaxCategory.tax_category()}?code={target_code}"
    response = requests.get(url, headers=auth_headers)
    log_request_response(url=url, response=response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    res_json = response.json()
    assert "hydra:member" in res_json, "'hydra:member' no está presente en la respuesta"
    assert isinstance(res_json["hydra:member"], list), "'hydra:member' no es una lista"
    assert any(cat["code"] == target_code for cat in res_json["hydra:member"]), (
        f"No se encontró una categoría con code = {target_code}"
    )


#TC_242: Iniciando verificación de campos no vacíos en tax categories
@pytest.mark.high
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.xfail(reason="known incumple con la validacion esperada del sistema BUG", run=True)
def test_TC242_get_tax_categories_valida_code_y_name_no_vacios(setup_teardown_view_tax_category):
    auth_headers, tax_category1, tax_category2 = setup_teardown_view_tax_category
    endpoint = EndpointTaxCategory.tax_category()
    response = SyliusRequest.get(endpoint, auth_headers)
    log_request_response(endpoint, response, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)

    categorias = response.json().get("hydra:member", [])
    ids_con_errores = []
    for categoria in categorias:
        if categoria.get("code", "").strip() == "" or categoria.get("name", "").strip() == "":
            ids_con_errores.append(categoria.get("id", categoria))
    assert not ids_con_errores, f"Las siguientes categorías tienen code o name vacío: {ids_con_errores}"


#TC_240: Iniciando test obteniendo token invalido o sin autenticacion
@pytest.mark.high
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC240_verificar_respuesta_token_invalido_o_sin_autenticacion():
    url = EndpointTaxCategory.tax_category()
    response = requests.get(url)  # Sin headers
    log_request_response(url=url, response=response)
    AssertionStatusCode.assert_status_code_401(response)


#TC_239: Iniciando test funcional obteniendo categoria de impuesto con un codigo inexistente
@pytest.mark.medium
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC239_tax_category_no_existe(auth_headers):
    non_existing_code = "NO_EXISTE"
    url = f"{EndpointTaxCategory.tax_category()}/{non_existing_code}"
    response = requests.get(url, headers=auth_headers)
    log_request_response(url, response, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)


#TC_243: Iniciando test de seguridad para Tax Categories - token expirado
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.high
@pytest.mark.security
def test_TC243_verificar_acceso_token_expirado_tax_category():
    expired_headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTQyMzQzODksImV4cCI6MTc1NDIzNzk4OSwicm9sZXMiOlsiUk9MRV9BRE1JTklTVFJBVElPTl9BQ0NFU1MiLCJST0xFX0FQSV9BQ0NFU1MiXSwidXNlcm5hbWUiOiJhcGkifQ.GmVMaimodyHNL8R9wToFg5RoOTwd9Rjf2WVqI_WoZJjAZJ1ykbaBlsbC4TWwPqZuaEpPhFJlRotqezn0_HF7MumgZBK1rvmfX4M7QqQBeeohmZmt8JB0eAjaqn-GtmmWeXrV1bCHxvqb-W1pbPsBQ1leKfnYeUnMPwrhPBsqdOAAEVK0ZWj_LAbgYWlViEZ8uw7qxDR5gzmd6GwKEawLDlMa9Lj5Hz8sG7NuYonU-b38U_mOkN57xr4SSL7DTkdk-q9rIOt-I056tzCKPR2Fx0CxCSO7MMP9pVN9sHMz53srPpHTvwtRCZSgzRB4PGU6mzsmfl4l7sLE72OouL-y_eVqgKJ-7YG5D_ZNp8vgaALqYDzbAySDb_ktFtCCWzhMxasoBOLoCzy3J1URprwxyPcYabntVyr8O42mkIjh1iGH-IASK9M614epkcBcSIbyB5cwkTwfBCAhMwqot6Ec6ozT8VKmfYAZdtisKpVarQrs25CRzdT1kZrRr57FsGgLQgf05K39QLM5wvjEd2i7NiRwCPVeqFVzJgBKN0DQBLK3a7zoN3a_mV7KCGmxoTk0RfYEhv00EpxVjMUWg40Cpg22YlFD1WZNxrN1r4Wt0LqkZfCfwPzD9Ci2X45oDjzPmIu6goaWDaaSgpaIeB6pxy-AuWi3ofhXlZkvlTgEm0"
    }
    endpoint = EndpointTaxCategory.tax_category()
    response = requests.get(endpoint, headers=expired_headers)
    log_request_response(endpoint, response, headers=expired_headers)
    AssertionStatusCode.assert_status_code_401(response)


# TC244 verficar headers de respuesta de tax category
@pytest.mark.high
@pytest.mark.negative
@pytest.mark.functional
def test_TC244_verificar_headers_respuesta_tax_category(setup_teardown_view_tax_category):
    auth_headers, tax_category1, tax_category2 = setup_teardown_view_tax_category
    endpoint = EndpointTaxCategory.tax_category()
    response = requests.get(endpoint, headers=auth_headers)
    log_request_response(endpoint, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)

    headers = response.headers

    content_type = headers.get("Content-Type", "")
    assert "application/ld+json" in content_type, (
        f"Content-Type debe ser 'application/ld+json'. Actual: {content_type}"
    )
    assert "Date" in headers, "Header 'Date' no encontrado"
    assert "Cache-Control" in headers, "Header 'Cache-Control' no encontrado"

    expected_security_headers = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY"
    }
    for header, expected_value in expected_security_headers.items():
        assert header in headers, f"Header de seguridad '{header}' no presente en la respuesta"
        assert headers["X-Frame-Options"] in ["DENY", "sameorigin"], (
            f"El valor de 'X-Frame-Options' debería ser 'DENY' o 'sameorigin'. Actual: '{headers['X-Frame-Options']}'"
        )