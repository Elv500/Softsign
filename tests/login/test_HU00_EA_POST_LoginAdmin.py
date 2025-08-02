import requests
import pytest

from src.routes.endpoint import Endpoint
from src.routes.request import SyliusRequest
from src.assertions.status_code_assertions import AssertionStatusCode
from src.resources.autentifications.autentificacion import Auth
from src.assertions.login_assertions import AssertionLogin


@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.regression
def test_TC55_Auth_exitoso_con_credenciales_validas():
    payload = Auth().get_valid_login_payload()
    response = SyliusRequest.post(Endpoint.login(), payload=payload)
    AssertionLogin.assert_login_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionLogin.assert_login_output_schema(response.json())

def test_TC56_Auth_fallido_con_credenciales_invalidas():
    payload = Auth().get_invalid_login_payload()
    response = SyliusRequest.post(Endpoint.login(), payload=payload)
    AssertionStatusCode.assert_status_code_401(response)

def test_TC57_Auth_fallido_con_email_invalida():
    payload = Auth().get_invalid_email_payload()
    response = SyliusRequest.post(Endpoint.login(), payload=payload)
    AssertionStatusCode.assert_status_code_401(response)

def test_TC58_Auth_fallido_con_password_invalida():
    payload = Auth().get_invalid_password_payload()
    response = SyliusRequest.post(Endpoint.login(), payload=payload)
    AssertionStatusCode.assert_status_code_401(response)

def test_TC59_Auth_fallido_con_crendenciales_vacias():
    payload = Auth().get_empty_credential_payload()
    response = SyliusRequest.post(Endpoint.login(), payload=payload)
    AssertionStatusCode.assert_status_code_400(response)

def test_TC60_Auth_fallido_con_email_vacia():
    payload = Auth().get_empty_email_payload()
    response = SyliusRequest.post(Endpoint.login(), payload=payload)
    AssertionStatusCode.assert_status_code_400(response)

def test_TC61_Auth_fallido_con_password_vacia():
    payload = Auth().get_empty_password_payload()
    response = SyliusRequest.post(Endpoint.login(), payload=payload)
    AssertionStatusCode.assert_status_code_400(response)