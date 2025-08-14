import pytest

from src.assertions.association_types_assertions import AssertionAssociationTypes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_product_association import EndpointAssociationTypes
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.regression
def test_TC379_eliminar_tipo_asociacion_existente_por_codigo_exitoso_204(setup_association_types):
    headers, association_type = setup_association_types
    url = EndpointAssociationTypes.code(association_type['code'])

    response = SyliusRequest.delete(url, headers)
    log_request_response(url, response, headers)
    AssertionStatusCode.assert_status_code_204(response)

    response = SyliusRequest.get(url, headers)
    log_request_response(url, response, headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionAssociationTypes.assert_error_schema(response.json())


@pytest.mark.negative
@pytest.mark.regression
def test_TC380_eliminar_tipo_asociacion_codigo_inexistente_error_404(auth_headers):
    code_inexistente = "codigo-inexistente-123"
    url = EndpointAssociationTypes.code(code_inexistente)

    response = SyliusRequest.delete(url, auth_headers)
    log_request_response(url, response, auth_headers)

    AssertionStatusCode.assert_status_code_404(response)
    AssertionAssociationTypes.assert_error_schema(response.json())


@pytest.mark.security
@pytest.mark.negative
@pytest.mark.regression
def test_TC381_enviar_solicitud_sin_token_autorizacion_error_401(setup_association_types):
    _, association_type = setup_association_types
    url = EndpointAssociationTypes.code(association_type['code'])

    response = SyliusRequest.delete(url, headers={})
    log_request_response(url, response, {})

    AssertionStatusCode.assert_status_code_401(response)


@pytest.mark.security
@pytest.mark.negative
@pytest.mark.regression
def test_TC382_enviar_solicitud_con_token_invalido_error_401(setup_association_types):
    _, association_type = setup_association_types
    url = EndpointAssociationTypes.code(association_type['code'])
    headers = {"Authorization": "Bearer token_invalido_123456"}

    response = SyliusRequest.delete(url, headers)
    log_request_response(url, response, headers)

    AssertionStatusCode.assert_status_code_401(response)
    AssertionAssociationTypes.assert_invalid_jwt_error(response.json())


@pytest.mark.functional
@pytest.mark.regression
def test_TC383_eliminar_tipo_asociacion_ya_eliminado(setup_association_types):
    headers, association_type = setup_association_types
    url = EndpointAssociationTypes.code(association_type['code'])

    response = SyliusRequest.delete(url, headers)
    log_request_response(url, response, headers)
    AssertionStatusCode.assert_status_code_204(response)

    response_2 = SyliusRequest.delete(url, headers)
    log_request_response(url, response_2, headers)
    AssertionStatusCode.assert_status_code_404(response_2)
    AssertionAssociationTypes.assert_error_schema(response_2.json())


@pytest.mark.functional
@pytest.mark.regression
def test_TC384_enviar_solicitud_sin_header_accept(setup_association_types):
    headers, association_type = setup_association_types
    url = EndpointAssociationTypes.code(association_type['code'])

    headers_sin_accept = headers.copy()
    headers_sin_accept.pop('Accept', None)

    response = SyliusRequest.delete(url, headers_sin_accept)
    log_request_response(url, response, headers_sin_accept)
    AssertionStatusCode.assert_status_code_204(response)

    response = SyliusRequest.get(url, headers)
    log_request_response(url, response, headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionAssociationTypes.assert_error_schema(response.json())


@pytest.mark.negative
@pytest.mark.regression
def test_TC385_eliminar_tipo_asociacion_usando_id_en_vez_de_code_error_404(setup_association_types):
    headers, association_type = setup_association_types
    url = EndpointAssociationTypes.code(association_type['id'])

    response = SyliusRequest.delete(url, headers)
    log_request_response(url, response, headers)

    AssertionStatusCode.assert_status_code_404(response)
    AssertionAssociationTypes.assert_error_schema(response.json())
