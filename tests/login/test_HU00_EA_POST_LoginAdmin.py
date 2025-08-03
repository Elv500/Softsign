import pytest

from src.routes.endpoint import Endpoint
from src.routes.request import SyliusRequest
from src.assertions.status_code_assertions import AssertionStatusCode
from src.resources.autentifications.autentificacion import Auth
from src.assertions.login_assertions import AssertionLogin
from utils.logger_helpers import log_request_response

@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.functional
def test_TC55_Auth_exitoso_con_credenciales_validas():
    payload = Auth().get_valid_login_payload()
    url = Endpoint.login()
    response = SyliusRequest.post(url, payload=payload)
    AssertionLogin.assert_login_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionLogin.assert_login_output_schema(response.json())
    log_request_response(url, response, payload=payload)

@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.functional
def test_TC56_Auth_fallido_con_credenciales_invalidas():
    url = Endpoint.login()
    payload = Auth().get_invalid_login_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(url, response, payload=payload)

@pytest.mark.login
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.functional
def test_TC57_Auth_fallido_con_email_invalida():
    url = Endpoint.login()
    payload = Auth().get_invalid_email_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(url, response, payload=payload)

@pytest.mark.login
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.functional
def test_TC58_Auth_fallido_con_password_invalida():
    url = Endpoint.login()
    payload = Auth().get_invalid_password_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(url, response, payload=payload)

@pytest.mark.login
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.functional
def test_TC59_Auth_fallido_con_crendenciales_vacias():
    url = Endpoint.login()
    payload = Auth().get_empty_credential_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(url, response, payload=payload)

@pytest.mark.login
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.functional
def test_TC151_Auth_fallido_con_email_vacia():
    url = Endpoint.login()
    payload = Auth().get_empty_email_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(url, response, payload=payload)

@pytest.mark.login
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.functional
def test_TC152_Auth_fallido_con_password_vacia():
    url = Endpoint.login()
    payload = Auth().get_empty_password_payload()
    response = SyliusRequest.post(url, payload=payload)
    AssertionStatusCode.assert_status_code_400(response)
    log_request_response(url, response, payload=payload)