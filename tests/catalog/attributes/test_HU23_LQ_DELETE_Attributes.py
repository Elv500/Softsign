import pytest
import time

from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from src.data.attributes import generate_attributes_source_data
from utils.logger_helpers import log_request_response

@pytest.mark.high
@pytest.mark.functional
@pytest.mark.smoke
#Admin> Catalog> Attributes TC_138: Se debe permitir eliminar un atributo existente.
def test_TC138_Verificar_eliminar_atributo_existente(auth_headers):

    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    create_response = SyliusRequest.post(url, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)
    attributes_code = create_response.json()["code"]
    endpoint = EndpointAttributes.code(attributes_code)
    response = SyliusRequest.delete(endpoint, auth_headers)
    log_request_response(endpoint, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(response)

@pytest.mark.high
@pytest.mark.functional
@pytest.mark.smoke
#Admin> Catalog> Attributes TC_139: No se debe permitir eliminar un atributo con code inexistente.
def test_TC139_Verificar_que_no_se_permita_eliminar_atributo_con_code_inexistente(auth_headers):
    code_inexistente = "000" #code inexistente
    endpoint = EndpointAttributes.code(code_inexistente)
    response = SyliusRequest.delete(endpoint, auth_headers)
    log_request_response(endpoint, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_404(response)


@pytest.mark.high
@pytest.mark.security
@pytest.mark.negative
#Admin> Catalog> Attributes TC_140: No se debe permitir eliminar un atributo sin autenticacion del token.
def test_TC140_Verificar_que_no_se_permita_eliminar_atributo_sin_token():
    code_existe = "t_shirt_brand"
    url = EndpointAttributes.code(code_existe)
    response = SyliusRequest.delete(url, {})
    log_request_response(url, response, headers={})
    AssertionStatusCode.assert_status_code_401(response)

@pytest.mark.high
@pytest.mark.smoke
@pytest.mark.functional
#Admin> Catalog> Attributes TC_405: Validar headers-response despues de eliminar el atributo.
def test_TC405_verificar_los_headers_respuesta_despues_de_eliminar_atributo(auth_headers):
    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    create_response = SyliusRequest.post(url, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)
    attributes_code = create_response.json()["code"]
    endpoint = EndpointAttributes.code(attributes_code)
    response = SyliusRequest.delete(endpoint, auth_headers)

    log_request_response(endpoint, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(response)
    assert response.content == b"" or len(response.content) == 0


@pytest.mark.high
@pytest.mark.functional
@pytest.mark.smoke
#Admin> Catalog> Attributes TC_406: El atributo eliminado no debe obtenerse con un GET.
def test_TC406_Verificar_que_el_atributo_eliminado_no_se_muestre(auth_headers):
    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    create_response = SyliusRequest.post(url, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)

    attributes_code = create_response.json()["code"]

    delete_endpoint = EndpointAttributes.code(attributes_code)
    delete_response = SyliusRequest.delete(delete_endpoint, auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)

    get_endpoint = EndpointAttributes.code(attributes_code)
    get_response = SyliusRequest.get(get_endpoint, auth_headers)

    log_request_response(get_endpoint, get_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_404(get_response)

@pytest.mark.high
@pytest.mark.security
@pytest.mark.smoke
#Admin> Catalog> Attributes TC_407: No debe eliminarse un atributo cuando se genera un token invalido.
def test_TC407_Verificar_no_permitir_eliminar_atributo_con_token_invalido():
    code_existe = "t_shirt_brand"
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    url = EndpointAttributes.code(code_existe)
    response = SyliusRequest.delete(url, invalid_headers)

    log_request_response(url, response, headers=invalid_headers)
    AssertionStatusCode.assert_status_code_401(response)


@pytest.mark.medium
@pytest.mark.performance
#Admin> Catalog> Attributes TC_408: El tiempo de respuesta despues de eliminar un atributo debe ser menor a 5 sec.
def test_TC408_verificar_el_tiempo_respuesta_despues_de_eliminar_atributo(auth_headers):
    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    create_response = SyliusRequest.post(url, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)
    attributes_code = create_response.json()["code"]

    start_time = time.time()
    endpoint = EndpointAttributes.code(attributes_code)
    response = SyliusRequest.delete(endpoint, auth_headers)
    elapsed = time.time() - start_time
    log_request_response(endpoint, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(response)
    assert elapsed < 5.0


@pytest.mark.high
@pytest.mark.functional
@pytest.mark.smoke
#Admin> Catalog> Attributes TC_409: No se debe permitir eliminar un atributo por segunda.
def test_TC409_Verificar_que_no_se_permita_eliminar_un_atributo_por_segunda_vez(auth_headers):
        data = generate_attributes_source_data()
        url = EndpointAttributes.attributes()
        create_response = SyliusRequest.post(url, auth_headers, data)
        AssertionStatusCode.assert_status_code_201(create_response)
        attributes_code = create_response.json()["code"]
        endpoint = EndpointAttributes.code(attributes_code)
        first_delete_response = SyliusRequest.delete(endpoint, auth_headers)
        AssertionStatusCode.assert_status_code_204(first_delete_response)
        second_delete_response = SyliusRequest.delete(endpoint, auth_headers)
        log_request_response(endpoint, second_delete_response, headers=auth_headers)
        AssertionStatusCode.assert_status_code_404(second_delete_response)