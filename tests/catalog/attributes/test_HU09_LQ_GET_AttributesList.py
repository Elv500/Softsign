import logging
import pytest
import time

from src.assertions.attributes_assertions import AssertionAttributes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from src.data.attributes import generate_attributes_source_data
from utils.logger_helpers import log_request_response

# Configurar logger
logger = logging.getLogger(__name__)


# Verificar que se pueda obterner la lista de los atributos  registrados en el submenu catálogo
# de la aplicacion Sylius.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC38_Verificar_que_se_obtenga_la_lista_atributos_registrados(auth_headers):
    logger.info("=== TC_38: Iniciando test para obtener lista de atributos registrados en Sylius ===")

    endpoint = EndpointAttributes.attributes()
    response = SyliusRequest.get(endpoint, auth_headers)

    log_request_response(endpoint, response, headers=auth_headers)

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAttributes.assert_attributes_get_output_schema(response.json())


#Verificar que se pueda obtener un atributo cuando se realiza la busqueda por su campo code
@pytest.mark.functional
@pytest.mark.smoke
def test_TC39_Verificar_que_obtenga_un_atributo_por_code(auth_headers):
    attribute_code = "retail"
    logger.info(f"=== TC_39: Iniciando test para obtener un atributo específico: {attribute_code} ===")

    # Crear el atributo si no existe
    data = generate_attributes_source_data()
    data["code"] = attribute_code
    SyliusRequest.post(EndpointAttributes.attributes(), auth_headers, data)

    endpoint = EndpointAttributes.code(attribute_code)
    response = SyliusRequest.get(endpoint, auth_headers)

    log_request_response(endpoint, response, headers=auth_headers)

    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["code"] == attribute_code


#Verificar que se muestre un error 404 cuando se intenta realizar la busqueda de un atributo
# por un code inexistente
@pytest.mark.negative
@pytest.mark.smoke
def test_TC41_Verificar_que_no_se_permita_obtener_un_atributo_code_inexistente(auth_headers):
    code_inexistente = "codigo_inexistente_123"
    logger.info(f"=== TC_41: Iniciando test con code inexistente: {code_inexistente} ===")

    url = EndpointAttributes.code(code_inexistente)
    response = SyliusRequest.get(url, auth_headers)

    log_request_response(url, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_404(response)


# Verificar que no se muestre la lista de atributos cuando no se genero el token correctamete
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC40_Verificar_que_no_se_permita_obtener_la_lista_de_atributos_sin_token():
    logger.info("=== TC_40: Iniciando el test de seguridad - obtener lista de atributos sin token ===")

    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, {})

    log_request_response(url, response, headers={})

    AssertionStatusCode.assert_status_code_401(response)


#Verificar la paginación de la lista atributos registardos en Syluis
@pytest.mark.functional
@pytest.mark.smoke
def test_TC42_Verificar_la_paginacion_de_la_lista_de_atributos(auth_headers):
    page, items_per_page = 1, 2
    logger.info(f"=== TC_42: Iniciando test de paginación de atributos (page={page}, itemsPerPage={items_per_page}) ===")

    url = EndpointAttributes.attributes_with_params(page=page, itemsPerPage=items_per_page)
    response = SyliusRequest.get(url, auth_headers)

    log_request_response(url, response, headers=auth_headers)

    AssertionStatusCode.assert_status_code_200(response)
    atributos = response.json().get("hydra:member", [])
    logger.info(f"Cantidad de atributos recibidos: {len(atributos)}")
    assert len(atributos) <= items_per_page


#Verificar headers de respuesta del GET de atributos
@pytest.mark.functional
@pytest.mark.smoke
def test_TC201_verificar_headers_respuesta_del_metodo_get_atributos(auth_headers):
    logger.info("=== TC_201: Iniciando verificación de headers HTTP del método GET de atributos ===")

    endpoint = EndpointAttributes.attributes()
    response = SyliusRequest.get(endpoint, auth_headers)

    log_request_response(endpoint, response, headers=auth_headers)

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
    logger.info("=== TC_200: Iniciando verificación de schema del método GET de atributos ===")

    endpoint = EndpointAttributes.attributes()
    response = SyliusRequest.get(endpoint, auth_headers)

    log_request_response(endpoint, response, headers=auth_headers)

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAttributes.assert_attributes_get_output_schema(response.json())


#Verificar que no se obtenga el atributo si se realiza la busqueda con un codigo que no existe
#Verificar que se muestre un error 404
@pytest.mark.negative
@pytest.mark.smoke
def test_TC202_Verificar_que_no_se_obtenga_la_lista_atributos_con_codigo_inexistente(auth_headers):
    code_inexistente = "codigo_inexistente_123"
    logger.info(f"=== TC_202: Iniciando test con code inexistente: {code_inexistente} ===")

    endpoint = EndpointAttributes.code(code_inexistente)
    response = SyliusRequest.get(endpoint, auth_headers)

    log_request_response(endpoint, response, headers=auth_headers)

    AssertionStatusCode.assert_status_code_404(response)


#Verificar que no se obtenga la lista de atributos si no se genera el tocken existosamente
#Verificar que se muestre un error 401
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC203_Verificar_que_no_se_obtenga_lista_de_atributos_sin_token():
    logger.info("=== TC_203: Iniciando test de seguridad - obtener lista de atributos sin token ===")

    endpoint = EndpointAttributes.attributes()
    response = SyliusRequest.get(endpoint, {})

    log_request_response(endpoint, response, headers={})

    AssertionStatusCode.assert_status_code_401(response)


#Verificar que no se obtenga la lista de atributos si se genera el token invalido
#Verificar que se muestre un error 401
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC204_Verificar_que_no_se_obtenga_lista_de_atributos_con_token_invalido():
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    logger.info("=== TC_204: Iniciando test de seguridad - token inválido ===")
    logger.info(f"Token usado: {invalid_headers['Authorization'][:20]}...")

    endpoint = EndpointAttributes.attributes()
    response = SyliusRequest.get(endpoint, invalid_headers)

    log_request_response(endpoint, response, headers=invalid_headers)

    AssertionStatusCode.assert_status_code_401(response)


