import requests
import pytest

from src.assertions.options_assertions import AssertionOptions
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_options import EndpointOptions
from src.routes.request import SyliusRequest
from utils.config import BASE_URL

@pytest.mark.functional
@pytest.mark.smoke
def test_TC103_Validar_la_estructura_JSON_de_la_respuesta(auth_headers):
    """Este test case verifica que el endpoint GET /admin/product-options retorne una respuesta con
    código de estado HTTP 200 (éxito) y que la estructura del JSON cumpla con el esquema esperado"""
    response = SyliusRequest.get(EndpointOptions.options(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionOptions.assert_options_list_schema(response.json())

@pytest.mark.functional
@pytest.mark.negative
def test_TC104_Verificar_respuesta_401_sin_token_de_autenticacion():
    """Verifica que el endpoint /admin/product-options requiera autenticación,
    devolviendo un código 401 cuando no se proporciona token de acceso."""
    response = SyliusRequest.get(EndpointOptions.options(),{})
    AssertionStatusCode.assert_status_code_401(response)

@pytest.mark.functional
@pytest.mark.negative
def test_TC149_Verificar_respuesta_401_con_token_de_autenticacion_invalido():
    """Verifica que el endpoint /admin/product-options devuelva un código 401 cuando se
    intenta acceder con un token inválido."""
    headers = {"Authorization": "Token_invalido"}
    response = SyliusRequest.get(EndpointOptions.options(), headers)
    AssertionStatusCode.assert_status_code_401(response)

@pytest.mark.functional
@pytest.mark.smoke
def test_TC105_Verificar_error_404_al_buscar_codigo_inexistente(auth_headers):
    """Verificar que la API devuelva un codigo 404 cuando se consultan
    opciones de producto con un filtro de código inexistente."""
    options_code = "OpcionInexistente"
    response = SyliusRequest.get(EndpointOptions.code(options_code), auth_headers)
    AssertionStatusCode.assert_status_code_404(response)

@pytest.mark.functional
@pytest.mark.smoke
def test_TC106_Verificar_que_busqueda_por_codigo_exitoso_sea_exitosa(auth_headers):
    """Validar que el endpoint de opciones filtre correctamente cuando se busca por un código existente,
    devolviendo la opción correspondiente con el código exacto."""
    options_code = "dress_size"
    response = SyliusRequest.get(EndpointOptions.code(options_code),auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["code"] == options_code

@pytest.mark.functional
@pytest.mark.positive
def test_TC107_Verificar_que_busqueda_por_nombre_sea_exitosa(auth_headers):
    """Verifica que el endpoint de opciones filtre correctamente cuando se busca por un nombre existente,
    devolviendo correctamente todas las opciones que coincidan con el nombre proporcionado."""
    test_name = "Dress size"  # Ejemplo de nombre que existe en el sistema
    url = f"{BASE_URL}/admin/product-options"
    params = {"name": "Dress size"}
    response = requests.get(url, headers=auth_headers, params=params)
    AssertionStatusCode.assert_status_code_200(response)
    assert any(item["name"] == test_name
               for item in response.json()["hydra:member"])
