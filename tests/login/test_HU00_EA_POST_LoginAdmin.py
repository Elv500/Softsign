import requests
import pytest

import jsonschema
from jsonschema.exceptions import ValidationError

from src.routes.endpoint import Endpoint
from src.routes.request import SyliusRequest
from src.assertions.status_code_assertions import AssertionStatusCode
from src.resources.autentifications.autentificacion import Auth

from utils.config import BASE_URL

@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.regression
def test_TC55_Login_exitoso_con_credenciales_validas():
    payload = Auth().get_valid_login_payload()
    response = SyliusRequest.post(Endpoint.login(), payload=payload)
    AssertionStatusCode.assert_status_code_200(response)

def test_TC56_Login_fallido_con_credenciales_invalidas():
    payload = Auth().get_invalid_login_payload()
    response = SyliusRequest.post(Endpoint.login(), payload=payload)
    AssertionStatusCode.assert_status_code_401(response)