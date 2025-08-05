import pytest
import logging

from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from src.data.attributes import generate_attributes_source_data
from utils.logger_helpers import log_request_response

logger = logging.getLogger(__name__)

#Verificar que NO se pueda permita realizar la actualizacion si el atributo no existe.
#Verificar que se muestre un error 404 si se intenta actualizar un atributo que no existe.
@pytest.mark.negative
@pytest.mark.regression
def test_TC47_Verificar_que_no_permitar_actualizar_un_atributo_inexistente(auth_headers):
    logger.info("=== TC_47: Iniciando test - actualizar atributo inexistente ===")
    update_data = generate_attributes_source_data()
    url = EndpointAttributes.code("codigo_inexistente_123")
    put_response = SyliusRequest.put(url, auth_headers, update_data)
    log_request_response(url, put_response, headers=auth_headers, payload=update_data)
    AssertionStatusCode.assert_status_code_404(put_response)


#Verificar que NO se permita actualizar un atributo sin averse generado el token.
#Verificar que se muestre un error 401.
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC48_Verificar_que_no_se_permita_actualizar_atributo_sin_token():
    logger.info("=== TC_48: Iniciando test de seguridad - actualizar atributo sin token ===")
    update_data = generate_attributes_source_data()
    url = EndpointAttributes.code("codigo_inexistente_123")
    put_response = SyliusRequest.put(url, {}, update_data)
    log_request_response(url, put_response, headers={}, payload=update_data)
    AssertionStatusCode.assert_status_code_401(put_response)


#Verificar que NO se permita actualizar un atributo con datos invalidos como un espacio en blanco.
#Verificar que se muestre un error 422.
@pytest.mark.negative
@pytest.mark.smok
def test_TC233_Verificar_que_no_se_actualice_atributo_con_datos_invalidos(auth_headers):
    logger.info("=== TC_233: Iniciando test - actualizar atributo con datos inválidos ===")
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
