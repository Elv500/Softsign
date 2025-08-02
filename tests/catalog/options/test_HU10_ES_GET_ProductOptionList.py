import requests
import pytest

from src.assertions.options_assertions import AssertionOptions
from src.assertions.status_code_assertions import AssertionStatusCode
from utils.config import BASE_URL

@pytest.mark.funcional
@pytest.mark.smoke
def test_TC103_Validar_la_estructura_JSON_de_la_respuesta(auth_headers):
    """Este test case verifica que el endpoint GET /admin/product-options retorne una respuesta con
    código de estado HTTP 200 (éxito) y que la estructura del JSON cumpla con el esquema esperado"""
    url = f"{BASE_URL}/admin/product-options"
    response = requests.get(url, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionOptions.assert_options_list_schema(response.json())



@pytest.mark.funcional
@pytest.mark.negative
def test_TC104_Verificar_respuesta_401_sin_token_de_autenticacion():
    """Verifica que el endpoint /admin/product-options requiera autenticación,
    devolviendo un código 401 cuando no se proporciona token de acceso."""
    url = f"{BASE_URL}/admin/product-options"
    response = requests.get(url, headers={}, params=None)
    AssertionStatusCode.assert_status_code_401(response)

@pytest.mark.funcional
@pytest.mark.negative
def test_TC149_Verificar_respuesta_401_con_token_de_autenticacion_invalido():
    """Verifica que el endpoint /admin/product-options devuelva un código 401 cuando se
    intenta acceder con un token inválido."""
    url = f"{BASE_URL}/admin/product-options"
    headers = {"Authorization": "Token_invalido"}
    response = requests.get(url, headers=headers)
    AssertionStatusCode.assert_status_code_401(response)

@pytest.mark.funcional
@pytest.mark.positive
def test_TC105_Verificar_respuesta_vacía_al_buscar_opción_inexistente(auth_headers):
    """Verificar que la API devuelva correctamente una respuesta vacía cuando se consultan
    opciones de producto con un filtro de código inexistente."""

    # Buscar una opción que no exista
    url = f"{BASE_URL}/admin/product-options"
    params = {"code": "opcion_inexistente_12345"}
    response = requests.get(url, headers=auth_headers, params=params)

    AssertionStatusCode.assert_status_code_200(response)
    assert len(response.json().get("hydra:member", [])) == 0
    assert response.json()["hydra:totalItems"] == 0


@pytest.mark.funcional
@pytest.mark.positive
def test_TC106_Verificar_que_busqueda_por_nombre_sea_exitosa(auth_headers):
    """Verifica que el filtro por nombre devuelve coincidencias exactas"""
    test_name = "Dress size"  # Ejemplo de nombre que existe en el sistema

    url = f"{BASE_URL}/admin/product-options"
    params = {"name": "Dress size"}
    response = requests.get(url, headers=auth_headers, params=params)

    AssertionStatusCode.assert_status_code_200(response)
    assert any(item["name"] == test_name
               for item in response.json()["hydra:member"])


@pytest.mark.funcional
@pytest.mark.positive
def test_TC107_Verificar_que_busqueda_por_codigo_sea_exitosa(auth_headers):
    """Verifica que el filtro por codigo devuelve coincidencias exactas"""
    test_code = "dress_size"  # Ejemplo de nombre que existe en el sistema

    url = f"{BASE_URL}/admin/product-options"
    params = {"code": "dress_size"}
    response = requests.get(url, headers=auth_headers, params=params)

    AssertionStatusCode.assert_status_code_200(response)
    assert any(item["code"] == test_code
               for item in response.json()["hydra:member"])








