import pytest
import logging

from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from src.data.attributes import generate_attributes_source_data
from utils.logger_helpers import log_request_response


#Admin> Catalog> Attributes TC_47: No se debe permitir actualizar si el atributo no existe.
@pytest.mark.negative
@pytest.mark.regression
def test_TC47_Verificar_que_no_permitar_actualizar_un_atributo_inexistente(auth_headers):
    update_data = generate_attributes_source_data()
    url = EndpointAttributes.code("codigo_inexistente_123")
    put_response = SyliusRequest.put(url, auth_headers, update_data)
    log_request_response(url, put_response, headers=auth_headers, payload=update_data)
    AssertionStatusCode.assert_status_code_404(put_response)


#Admin> Catalog> Attributes TC_48: No se debe permitir actualizar un atributo sin token.
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC48_Verificar_que_no_se_permita_actualizar_atributo_sin_token():
    update_data = generate_attributes_source_data()
    url = EndpointAttributes.code("codigo_inexistente_123")
    put_response = SyliusRequest.put(url, {}, update_data)
    log_request_response(url, put_response, headers={}, payload=update_data)
    AssertionStatusCode.assert_status_code_401(put_response)


#Admin> Catalog> Attributes TC_233: No se debe actualizar el atributo con data invalida.
@pytest.mark.negative
@pytest.mark.smok
def test_TC233_Verificar_que_no_se_actualice_atributo_con_datos_invalidos(auth_headers):
    data = generate_attributes_source_data()
    post_response = SyliusRequest.post(EndpointAttributes.attributes(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(post_response)
    code = post_response.json()["code"]

    update_data = data.copy()
    update_data["translations"]["en_US"]["name"] = ""
    url = EndpointAttributes.code(code)
    put_response = SyliusRequest.put(url, auth_headers, update_data)
    log_request_response(url, put_response, headers=auth_headers, payload=update_data)
    AssertionStatusCode.assert_status_code_422(put_response)
