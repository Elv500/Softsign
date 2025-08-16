import pytest

from src.routes.endpoint import Endpoint
from src.routes.request import SyliusRequest
from src.assertions.status_code_assertions import AssertionStatusCode
from src.resources.autentifications.autentificacion import Auth
from src.assertions.login_assertions import AssertionLogin
from utils.logger_helpers import log_request_response


#TC-55: Login > Admin - Autenticación exitosa usando email y contraseña válidos
@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.high
def test_TC55_Auth_exitoso_con_credenciales_validas():
    payload = Auth().get_valid_login_payload()
    url = Endpoint.login()
    response = SyliusRequest.post(url, payload=payload)
    AssertionLogin.assert_login_input_schema(payload)
    assert payload["email"] is not None
    assert payload["password"] is not None
    AssertionStatusCode.assert_status_code_200(response)
    AssertionLogin.assert_login_output_schema(response.json())
    assert response.json()["token"] is not None
    assert response.json()["adminUser"] is not None
    log_request_response(url, response, payload=payload)


#TC-56: Login > Admin - Autenticación fallida con email y contraseña inválidos
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.high
def test_TC56_Auth_fallido_con_credenciales_invalidas():
    url = Endpoint.login()
    payload = Auth().get_invalid_login_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionLogin.assert_login_input_schema(payload)
    assert payload["email"] is not None
    assert payload["password"] is not None
    AssertionStatusCode.assert_status_code_401(response)
    assert response.json()["code"] == 401
    assert response.json()["message"] == 'Invalid credentials.'
    log_request_response(url, response, payload=payload)


#TC-57: Login > Admin - Autenticación fallida con email inválido y contraseña válida
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.high
def test_TC57_Auth_fallido_con_email_invalida():
    url = Endpoint.login()
    payload = Auth().get_invalid_email_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionLogin.assert_login_input_schema(payload)
    assert payload["email"] is not None
    assert payload["password"] is not None
    AssertionStatusCode.assert_status_code_401(response)
    assert response.json()["code"] == 401
    assert response.json()["message"] == 'Invalid credentials.'
    log_request_response(url, response, payload=payload)


#TC-58: Login > Admin - Autenticación fallida con email válido y contraseña inválida
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.high
def test_TC58_Auth_fallido_con_password_invalida():
    url = Endpoint.login()
    payload = Auth().get_invalid_password_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionLogin.assert_login_input_schema(payload)
    assert payload["email"] is not None
    assert payload["password"] is not None
    AssertionStatusCode.assert_status_code_401(response)
    assert response.json()["code"] == 401
    assert response.json()["message"] == 'Invalid credentials.'
    log_request_response(url, response, payload=payload)


#TC-59: Login > Admin - Autenticación fallida con email y contraseña vacíos
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.high
def test_TC59_Auth_fallido_con_crendenciales_vacias():
    url = Endpoint.login()
    payload = Auth().get_empty_credential_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionLogin.assert_login_input_schema(payload)
    assert payload["email"] is not None
    assert payload["password"] is not None
    AssertionStatusCode.assert_status_code_400(response)
    assert response.json()["code"] == 400
    assert response.json()["message"] == 'Bad Request'
    log_request_response(url, response, payload=payload)


#TC-151: Login > Admin - Autenticación fallida con email vacío y contraseña válida
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.high
def test_TC151_Auth_fallido_con_email_vacia():
    url = Endpoint.login()
    payload = Auth().get_empty_email_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionLogin.assert_login_input_schema(payload)
    assert payload["email"] is not None
    assert payload["password"] is not None
    AssertionStatusCode.assert_status_code_400(response)
    assert response.json()["code"] == 400
    assert response.json()["message"] == 'Bad Request'
    log_request_response(url, response, payload=payload)


#TC-152: Login > Admin - Autenticación fallida con contraseña vacía y email válido
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.high
def test_TC152_Auth_fallido_con_password_vacia():
    url = Endpoint.login()
    payload = Auth().get_empty_password_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionLogin.assert_login_input_schema(payload)
    assert payload["email"] is not None
    assert payload["password"] is not None
    AssertionStatusCode.assert_status_code_400(response)
    assert response.json()["code"] == 400
    assert response.json()["message"] == 'Bad Request'
    log_request_response(url, response, payload=payload)