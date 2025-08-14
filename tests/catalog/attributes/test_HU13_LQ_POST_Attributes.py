import pytest
import time

from src.assertions.attributes_assertions import AssertionAttributes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from src.data.attributes import generate_attributes_source_data
from utils.logger_helpers import log_request_response


@pytest.mark.smoke
@pytest.mark.functional
# Admin> Catalog> Attributes> TC_49:Crear un nuevo atributo dentro de catalagos.
def test_TC49_Verificar_que_se_permita_crear_nuevo_atributo(setup_add_attributes):
    headers, created_attributes = setup_add_attributes
    data = generate_attributes_source_data()
    response = SyliusRequest.post(EndpointAttributes.attributes(), headers, data)
    log_request_response(EndpointAttributes.attributes(), response, headers, data)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionAttributes.assert_attributes_post_output_schema(response.json())
    created_attributes.append(response.json())


# Admin> Catalog> Attributes> TC_50: Despues de crear un atributo validar la estructura del JSON.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC50_Verificar_la_estructura_json_response_despues_de_crear_atributp(setup_attributes_cleanup):
    auth_headers, add_attributes_for_cleanup = setup_attributes_cleanup

    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    response = SyliusRequest.post(url, auth_headers, data)
    log_request_response(url, response, headers=auth_headers, payload=data)

    AssertionStatusCode.assert_status_code_201(response)
    AssertionAttributes.assert_attributes_post_output_schema(response.json())
    attributes_code = response.json()["code"]
    add_attributes_for_cleanup(attributes_code)


# Admin> Catalog> Attributes> TC_51: No debe crearse un nuevo atributo sin el campo requerido name.
@pytest.mark.smoke
@pytest.mark.functional
def test_TC51_Verificar_no_crear_atributo_sin_campo_name(auth_headers):
    data = generate_attributes_source_data()
    del data["translations"]["en_US"]["name"]

    url = EndpointAttributes.attributes()
    response = SyliusRequest.post(url, auth_headers, data)

    log_request_response(url, response, headers=auth_headers, payload=data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin> Catalog> Attributes> TC_52: No debe crearse un nuevo atributo sin el campo  code.
@pytest.mark.smoke
@pytest.mark.functional
def test_TC52_Verificar_no_crear_atributo_sin_campo_code(auth_headers):
    data = generate_attributes_source_data()
    data["code"] = ""
    url = EndpointAttributes.attributes()
    response = SyliusRequest.post(url, auth_headers, data)

    log_request_response(url, response, headers=auth_headers, payload=data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin> Catalog> Attributes> TC_410: No debe crearse un nuevo atributo con una name mayor a 255 caracteres.
@pytest.mark.smoke
@pytest.mark.functional
def test_TC410_Verificar_no_crear_atributo_con_nombre_mayor_255caracteres(auth_headers):
    data = generate_attributes_source_data()
    data["translations"]["en_US"]["name"] = "a" * 256
    url = EndpointAttributes.attributes()
    response = SyliusRequest.post(url, auth_headers, data)

    log_request_response(url, response, headers=auth_headers, payload=data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin> Catalog> Attributes> TC_411: No debe crearse un nuevo atributo sin token de autenticacion.
@pytest.mark.smoke
@pytest.mark.security
def test_TC411_Verificar_no_crear_atributo_sin_token_autentication():
    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    response = SyliusRequest.post(url, {}, data)

    log_request_response(url, response, headers={}, payload=data)
    AssertionStatusCode.assert_status_code_401(response)


# Admin> Catalog> Attributes> TC_412: No debe crearse un nuevo atributo con token de invalido.
@pytest.mark.functional
@pytest.mark.security
def test_TC412_Verificar_no_crear_atributo_con_token_invalido():
    data = generate_attributes_source_data()
    invalid_token = {"Authorization": "Bearer token_invalido"}
    url = EndpointAttributes.attributes()
    response = SyliusRequest.post(url, invalid_token, data)

    log_request_response(url, response, headers=invalid_token, payload=data)
    AssertionStatusCode.assert_status_code_401(response)


# Admin> Catalog> Attributes> TC_413: El response time debe ser menor a 5 segundos.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC413_Verificar_tiempo_respuesta_creacion_de_un_atributo(setup_attributes_cleanup):
    auth_headers, add_attribute_for_cleanup = setup_attributes_cleanup

    data = generate_attributes_source_data()
    start_time = time.time()
    url = EndpointAttributes.attributes()
    response = SyliusRequest.post(url, auth_headers, data)
    elapsed = time.time() - start_time

    log_request_response(url, response, headers=auth_headers, payload=data)
    AssertionStatusCode.assert_status_code_201(response)
    assert elapsed < 5.0

    attributes_code = response.json()["code"]
    add_attribute_for_cleanup(attributes_code)


# Admin> Catalog> Attributes> TC_414: Verificar headers de respuesta despues de crear un atributo.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC414_Verificar_headers_respuesta_despues_de_crear_atributo(setup_attributes_cleanup):
    auth_headers, add_attributes_for_cleanup = setup_attributes_cleanup

    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    response = SyliusRequest.post(url, auth_headers, data)

    log_request_response(url, response, headers=auth_headers, payload=data)
    AssertionStatusCode.assert_status_code_201(response)

    headers = response.headers
    content_type = headers.get("Content-Type", "")
    assert content_type.startswith("application/ld+json"), f"Expected JSON-LD content type, got: {content_type}"

    attributes_code = response.json()["code"]
    add_attributes_for_cleanup(attributes_code)


# Admin> Catalog> Attributes> TC_415: No debe crearse un atributo si el JSON Body es incorrecto.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC415_Verificar_no_crear_atributo_json_incorrecto(auth_headers):
    import requests
    url = EndpointAttributes.attributes()
    response = requests.post(
        url,
        headers={**auth_headers, 'Content-Type': 'application/json'},
        data='{"code": "test", "name": invalid_json}'
    )

    log_request_response(url, response, headers={**auth_headers, 'Content-Type': 'application/json'})
    AssertionStatusCode.assert_status_code_400(response)
