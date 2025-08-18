import pytest

from src.assertions.options_assertions import AssertionOptions
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_options import EndpointOptions
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response

#Este test case verifica que el endpoint GET /admin/product-options retorne una respuesta con código de estado HTTP 200 (éxito) y que la estructura del JSON cumpla con el esquema esperado
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC103_Validar_la_estructura_JSON_de_la_respuesta(auth_headers):
    response = SyliusRequest.get(EndpointOptions.options(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionOptions.assert_options_list_schema(response.json())
    log_request_response(EndpointOptions.options(), response, auth_headers)

#Verifica que el endpoint /admin/product-options requiera autenticación, devolviendo un código 401 cuando no se proporciona token de acceso.
@pytest.mark.negative
@pytest.mark.smoke
@pytest.mark.high
def test_TC104_Verificar_respuesta_401_sin_token_de_autenticacion():
    response = SyliusRequest.get(EndpointOptions.options(),{})
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(EndpointOptions.options(), response, {})

#Verifica que el endpoint /admin/product-options devuelva un código 401 cuando se intenta acceder con un token inválido.
@pytest.mark.negative
@pytest.mark.smoke
@pytest.mark.high
def test_TC149_Verificar_respuesta_401_con_token_de_autenticacion_invalido():
    headers = {"Authorization": "Token_invalido"}
    response = SyliusRequest.get(EndpointOptions.options(), headers)
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(EndpointOptions.options(), response, headers)

#Verificar que la API devuelva un codigo 404 cuando se consultan opciones de producto con un filtro de código inexistente.
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.high
def test_TC105_Verificar_error_404_al_buscar_codigo_inexistente(auth_headers):
    options_code = "OpcionInexistente"
    endpoint = EndpointOptions.code(options_code)
    response = SyliusRequest.get(EndpointOptions.code(options_code), auth_headers)
    AssertionStatusCode.assert_status_code_404(response)
    log_request_response(endpoint, response, auth_headers)

#Validar que el endpoint de opciones filtre correctamente cuando se busca por un código existente, devolviendo la opción correspondiente con el código exacto.
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.medium
def test_TC106_Verificar_que_busqueda_por_codigo_exitoso_sea_exitosa(auth_headers):
    options_code = "dress_size"
    endpoint = EndpointOptions.code(options_code)
    response = SyliusRequest.get(EndpointOptions.code(options_code),auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["code"] == options_code
    log_request_response(endpoint, response, auth_headers)

#Verifica que el endpoint de opciones filtre correctamente cuando se busca por un nombre existente, devolviendo correctamente todas las opciones que coincidan con el nombre proporcionado.
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.medium
def test_TC107_Verificar_que_busqueda_por_nombre_sea_exitosa(auth_headers):
    name = "Dress size"  # Ejemplo de nombre que existe en el sistema
    endpoint = EndpointOptions.options_with_params(name=name)
    response = SyliusRequest.get(endpoint, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert any(item["name"] == name
               for item in response.json()["hydra:member"])
    log_request_response(endpoint, response, auth_headers)

#Verifica que el endpoint de opciones implemente correctamente la paginación, devolviendo el número correcto de elementos por página según los parámetros proporcionados.
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.medium
def test_TC245_Verificar_paginacion_de_lista_de_opciones(auth_headers):
    page = 1
    items_per_page = 10
    endpoint = EndpointOptions.options_with_params(page=page, itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert len(response.json().get("hydra:member", [])) <= items_per_page
    log_request_response(endpoint, response, auth_headers)

#Verifica que el endpoint de opciones maneje correctamente los parámetros de paginación inválidos, devolviendo un error 400 Bad Request.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.medium
def test_TC246_Verificar_paginacion_con_parametros_invalidos(auth_headers):
    page = -1  # Parámetro de página inválido
    items_per_page = -1  # Parámetro de elementos por página inválido
    endpoint = EndpointOptions.options_with_params(page=page, itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(endpoint, response, auth_headers)

#Verifica que el endpoint de opciones maneje correctamente un parámetro de página inválido, devolviendo un error 400 Bad Request.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.medium
def test_TC247_Verificar_paginacion_con_page_invalido(auth_headers):
    page = "invalid"  # Parámetro de página inválido
    items_per_page = 10  # Elementos por página válidos
    endpoint = EndpointOptions.options_with_params(page=page, itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    log_request_response(endpoint, response, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)

#Verifica que el endpoint de opciones maneje correctamente un parámetro de elementos por página inválido, devolviendo un error 400 Bad Request.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.medium
def test_TC248_Verificar_paginacion_con_items_per_page_invalido(auth_headers):
    page = 1  # Página válida
    items_per_page = -1  # Parámetro de elementos por página inválido
    endpoint = EndpointOptions.options_with_params(page=page, itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(endpoint, response, auth_headers)
