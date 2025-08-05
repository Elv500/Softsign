import json

import pytest

from src.assertions.association_types_assertions import AssertionAssociationTypes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_product_association import EndpointAssociationTypes
from src.routes.request import SyliusRequest
from src.data.association_types import generate_association_types_source_data
from utils.logger_helpers import log_request_response


@pytest.mark.smoke
@pytest.mark.regression
def test_TC120_crear_tipo_asociacion_code_y_translations_en_US_name_validos_exitoso(teardown_association_types):
    headers, created_inventories = teardown_association_types
    payload = generate_association_types_source_data()
    url = EndpointAssociationTypes.association_types()
    AssertionAssociationTypes.assert_association_type_add_input_schema(payload)

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()
    log_request_response(url, response, headers, payload)

    AssertionStatusCode.assert_status_code_201(response)
    AssertionAssociationTypes.assert_association_type_add_output_schema(response.json())
    AssertionAssociationTypes.assert_code_matches(response_data, payload['code'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "en_US",
                                                              payload['translations']['en_US']['name'])
    created_inventories.append(payload['code'])


@pytest.mark.smoke
@pytest.mark.regression
def test_TC121_crear_tipo_asociacion_multiples_traducciones_validas_en_US_es_ES_exitoso(teardown_association_types):
    headers, created_inventories = teardown_association_types
    payload = generate_association_types_source_data(include_es_ES=True, include_es_MX=True)
    url = EndpointAssociationTypes.association_types()
    AssertionAssociationTypes.assert_association_type_add_input_schema(payload)

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()
    log_request_response(url, response, headers, payload)

    AssertionStatusCode.assert_status_code_201(response)
    AssertionAssociationTypes.assert_association_type_add_output_schema(response.json())
    AssertionAssociationTypes.assert_code_matches(response_data, payload['code'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "en_US",
                                                              payload['translations']['en_US']['name'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "es_ES",
                                                              payload['translations']['es_ES']['name'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "es_MX",
                                                              payload['translations']['es_MX']['name'])
    created_inventories.append(payload['code'])


@pytest.mark.functional
@pytest.mark.regression
def test_TC122_validar_creacion_code_2_caracteres_exitoso(teardown_association_types):
    headers, created_inventories = teardown_association_types
    payload = generate_association_types_source_data(code="ab")
    url = EndpointAssociationTypes.association_types()
    AssertionAssociationTypes.assert_association_type_add_input_schema(payload)

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()
    log_request_response(url, response, headers, payload)

    AssertionStatusCode.assert_status_code_201(response)
    AssertionAssociationTypes.assert_association_type_add_output_schema(response.json())
    AssertionAssociationTypes.assert_code_matches(response_data, payload['code'])
    created_inventories.append(payload['code'])


@pytest.mark.functional
@pytest.mark.regression
def test_TC123_validar_creacion_code_255_caracteres_exitoso(teardown_association_types):
    headers, created_inventories = teardown_association_types
    code_255_chars = "a" * 255
    payload = generate_association_types_source_data(code=code_255_chars)
    url = EndpointAssociationTypes.association_types()
    AssertionAssociationTypes.assert_association_type_add_input_schema(payload)

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()
    log_request_response(url, response, headers, payload)

    AssertionStatusCode.assert_status_code_201(response)
    AssertionAssociationTypes.assert_association_type_add_output_schema(response_data)
    AssertionAssociationTypes.assert_code_matches(response_data, payload['code'])
    created_inventories.append(payload['code'])


@pytest.mark.regression
@pytest.mark.negative
def test_TC124_validar_error_code_1_caracter(auth_headers):
    headers = auth_headers
    payload = generate_association_types_source_data(code="a")
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()
    log_request_response(url, response, headers, payload)

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)
    AssertionAssociationTypes.assert_violation_message(response_data,
                                                       "Association type code must be at least 2 characters long.")


@pytest.mark.regression
@pytest.mark.negative
def test_TC125_validar_error_code_supera_255_caracteres(auth_headers):
    headers = auth_headers
    code_256_chars = "a" * 256
    payload = generate_association_types_source_data(code=code_256_chars)
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()
    log_request_response(url, response, headers, payload)

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)
    AssertionAssociationTypes.assert_violation_message(response_data,
                                                       "Association type code must not be longer than 255 characters.")


@pytest.mark.regression
@pytest.mark.negative
def test_TC126_validar_error_code_caracteres_invalidos(auth_headers):
    headers = auth_headers
    payload = generate_association_types_source_data(code=123)
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)

    AssertionStatusCode.assert_status_code_400(response)


@pytest.mark.regression
@pytest.mark.negative
def test_TC127_validar_error_code_ya_existe(teardown_association_types):
    headers, created_inventories = teardown_association_types
    payload = generate_association_types_source_data()
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    created_inventories.append(payload['code'])

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()
    log_request_response(url, response, headers, payload)

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)
    AssertionAssociationTypes.assert_violation_message(response_data,
                                                       "The association type with given code already exists.")


@pytest.mark.regression
@pytest.mark.negative
def test_TC128_validar_error_falta_campo_code(auth_headers):
    headers = auth_headers
    payload = generate_association_types_source_data()
    del payload['code']
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()
    log_request_response(url, response, headers, payload)

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)
    AssertionAssociationTypes.assert_violation_message(response_data,
                                                       "Please enter association type code.")
