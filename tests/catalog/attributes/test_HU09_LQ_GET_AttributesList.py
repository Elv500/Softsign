import pytest
import logging
import requests

from src.assertions.attributes_assertions import AssertionAttributes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response

# Configurar logger
logger = logging.getLogger(__name__)


# Verificar que se pueda obterner la lista de los atributos  registrados en el submenu catálogo
# de la aplicacion Sylius.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC38_Verificar_que_se_obtenga_la_lista_atributos_registrados(auth_headers):
    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, auth_headers)
    log_request_response(url, response, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionAttributes.assert_attributes_get_output_schema(response.json())


#Verificar que se pueda obtener un atributo cuando se realiza la busqueda por su campo code
@pytest.mark.functional
@pytest.mark.smoke
def test_TC39_Verificar_que_obtenga_un_atributo_por_code(auth_headers):
    code = "t_shirt_brand"
    url = EndpointAttributes.code(code)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["code"] == code


#Verificar que se muestre un error 404 cuando se intenta realizar la busqueda de un atributo
# por un code inexistente
@pytest.mark.negative
@pytest.mark.smoke
def test_TC41_Verificar_que_no_se_permita_obtener_un_atributo_code_inexistente(auth_headers):
    code_inexistente = "retail"
    url = EndpointAttributes.code(code_inexistente)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)
    log_request_response(url, response, auth_headers)


# Verificar que no se muestre la lista de atributos cuando no se genero el token correctamete
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC40_Verificar_que_no_se_permita_obtener_la_lista_de_atributos_sin_token():
    url = EndpointAttributes.attributes()
    response= SyliusRequest.get(url,{})
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(url, response)


#Verificar la paginación de la lista atributos registardos en Syluis
@pytest.mark.functional
@pytest.mark.smoke
def test_TC42_Verificar_la_paginacion_de_la_lista_de_atributos(auth_headers):
    page, items_per_page = 1, 2
    url = EndpointAttributes.attributes_with_params(page=page, itemsPerPage=items_per_page)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    atributos = response.json().get("hydra:member", [])
    logger.info(f"Cantidad de atributos recibidos: {len(atributos)}")
    assert len(atributos) <= items_per_page
    log_request_response(url, response)


#Verificar headers de respuesta del GET de atributos
@pytest.mark.functional
@pytest.mark.smoke
def test_TC201_verificar_headers_respuesta_del_metodo_get_atributos(auth_headers):
    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, auth_headers)
    log_request_response(url, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    headers = response.headers
    logger.info(f"Headers response recibido: {dict(headers)}")
    content_type = headers.get("Content-Type", "")
    logger.info(f"Content-Type: {content_type}")
    assert content_type.startswith("application/ld+json"), f"Expected JSON-LD content type, got: {content_type}"


# Validar el schema de respuesta del metodo GET
@pytest.mark.functional
@pytest.mark.smoke
def test_TC200_Verificar_el_schema_response_del_metodo_GET(auth_headers):
    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, auth_headers)
    log_request_response(url, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionAttributes.assert_attributes_get_output_schema(response.json())


#Verificar que no se obtenga el atributo si se realiza la busqueda con un codigo que no existe
#Verificar que se muestre un error 404
@pytest.mark.negative
@pytest.mark.smoke
def test_TC202_Verificar_que_no_se_obtenga_la_lista_atributos_con_type_inexistente(auth_headers):
    type = "type_inexistente"
    url = EndpointAttributes.code(type)
    response = SyliusRequest.get(url, auth_headers)
    log_request_response(url, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_404(response)


#Verificar que no se obtenga la lista de atributos si no se genera el tocken existosamente
#Verificar que se muestre un error 401
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC203_Verificar_que_no_se_obtenga_lista_de_atributos_sin_token():
    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, {})
    log_request_response(url, response, headers={})
    AssertionStatusCode.assert_status_code_401(response)


#Verificar que no se obtenga la lista de atributos si se genera el token invalido
#Verificar que se muestre un error 401
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC204_Verificar_que_no_se_obtenga_lista_de_atributos_con_token_invalido():
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, invalid_headers)
    log_request_response(url, response, headers=invalid_headers)
    AssertionStatusCode.assert_status_code_401(response)






