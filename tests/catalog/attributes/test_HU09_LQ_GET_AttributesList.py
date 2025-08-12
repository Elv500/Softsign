import pytest
import logging
import requests

from src.assertions.attributes_assertions import AssertionAttributes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response

#Admin> Catalog> Attributes TC_38: obtener la lista de atributos registrados.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC38_Verificar_que_se_obtenga_la_lista_atributos_registrados(auth_headers):
    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, auth_headers)
    log_request_response(url, response, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionAttributes.assert_attributes_get_output_schema(response.json())

#Admin> Catalog> Attributes TC_39: Obtener un atributo por su code.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC39_Verificar_que_se_obtenga_un_atributo_por_code(auth_headers):
    code = "t_shirt_brand"
    url = EndpointAttributes.code(code)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["code"] == code

#Admin> Catalog> Attributes TC_41: No se debe obtener ningun resultado si se ingreso un code que no existe.
@pytest.mark.negative
@pytest.mark.smoke
def test_TC41_Verificar_que_no_se_obtenga_un_atributo_code_inexistente(auth_headers):
    code_inexistente = "retail"
    url = EndpointAttributes.code(code_inexistente)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)
    log_request_response(url, response, auth_headers)


#Admin> Catalog> Attributes TC_40: No debe obtenerse la lista de atributos si la autenticacion fallo.
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC40_Verificar_que_no_se_permita_obtener_la_lista_de_atributos_sin_token():
    url = EndpointAttributes.attributes()
    response= SyliusRequest.get(url,{})
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(url, response)


#Admin> Catalog> Attributes TC_42: Validar la paginacion de la lista de atributos.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC42_Verificar_la_paginacion_de_la_lista_de_atributos(auth_headers):
    page, items_per_page = 1, 2
    url = EndpointAttributes.attributes_with_params(page=page, itemsPerPage=items_per_page)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    atributos = response.json().get("hydra:member", [])
    assert len(atributos) <= items_per_page
    log_request_response(url, response)


#Admin> Catalog> Attributes TC_201: Verificar los headers response del metodo GET.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC201_verificar_headers_respuesta_del_metodo_get_atributos(auth_headers):
    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, auth_headers)
    log_request_response(url, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    headers = response.headers
    content_type = headers.get("Content-Type", "")
    assert content_type.startswith("application/ld+json"), f"Expected JSON-LD content type, got: {content_type}"


#Admin> Catalog> Attributes TC_200: Verificar el schema response del metodo GET.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC200_Verificar_el_schema_response_del_metodo_GET(auth_headers):
    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, auth_headers)
    log_request_response(url, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionAttributes.assert_attributes_get_output_schema(response.json())


#Admin> Catalog> Attributes TC_202: Si el type no existe no debe obtenerse la lista de atributos.
@pytest.mark.smoke
def test_TC202_Verificar_que_no_se_obtenga_la_lista_atributos_con_type_inexistente(auth_headers):
    type = "type_inexistente"
    url = EndpointAttributes.code(type)
    response = SyliusRequest.get(url, auth_headers)
    log_request_response(url, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_404(response)


#Admin> Catalog> Attributes TC_204: No debe obtenerse la lista de atributos si se genera un token invalido.
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC204_Verificar_que_no_se_obtenga_lista_de_atributos_con_token_invalido():
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, invalid_headers)
    log_request_response(url, response, headers=invalid_headers)
    AssertionStatusCode.assert_status_code_401(response)
