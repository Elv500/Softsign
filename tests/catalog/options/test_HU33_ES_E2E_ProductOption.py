import pytest

from src.assertions.options_assertions import AssertionOptions
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_options import EndpointOptions
from src.routes.request import SyliusRequest
from src.data.options import generate_options_source_data, generate_updated_options_payload
from utils.logger_helpers import log_request_response

@pytest.mark.e2e
@pytest.mark.options
@pytest.mark.high
def test_HU33_E2E_ProductOption(setup_options_cleanup):
    headers, _ = setup_options_cleanup

    # Autenticarse con credenciales válidas y obtener token.
    # (Setup se encarga de esto y proporciona los headers con autenticación)

    # Listar opciones con autenticación válida.
    response = SyliusRequest.get(EndpointOptions.options(), headers)
    log_request_response(EndpointOptions.options(), response, headers)
    AssertionStatusCode.assert_status_code_200(response)

    # Crear una opción válida satisfactoriamente.
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)

    code = response.json()["code"]

    # Obtener la opción recién creada.
    response = SyliusRequest.get(EndpointOptions.code(code), headers)
    log_request_response(EndpointOptions.code(code), response, headers)
    AssertionStatusCode.assert_status_code_200(response)

    # Editar la opción creada satisfactoriamente.
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload(code, translation_id)
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_200(response)

    # Eliminar la opción creada satisfactoriamente.
    response = SyliusRequest().delete(EndpointOptions.code(code), headers)
    log_request_response(EndpointOptions.code(code), response, headers)
    AssertionStatusCode.assert_status_code_204(response)

    # Verificar que la opción eliminada no existe
    response = SyliusRequest.get(EndpointOptions.code(code), headers)
    log_request_response(EndpointOptions.code(code), response, headers)
    AssertionStatusCode.assert_status_code_404(response)