import pytest

from src.assertions.association_types_assertions import AssertionAssociationTypes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_product_association import EndpointAssociationTypes
from src.routes.request import SyliusRequest
from src.data.association_types import generate_association_type_translations_data, build_auth_headers
from utils.logger_helpers import log_request_response


@pytest.mark.smoke
@pytest.mark.regression
def test_TC364_modificar_traduccion_existente_en_US_pasando_id_exitoso(setup_teardown_association_types):
    headers, association_type1, _ = setup_teardown_association_types
    headers_general = build_auth_headers(headers.copy())
    url = EndpointAssociationTypes.code(association_type1['code'])
    en_us_id = association_type1["translations"]["en_US"]["@id"]
    payload = generate_association_type_translations_data(
        langs=["en_US"],
        overrides={"en_US": {"@id": en_us_id}}
    )

    response = SyliusRequest.put(url, headers_general, payload)
    response_data = response.json()
    log_request_response(url, response, headers_general, payload)

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_type_edit_output_schema(response.json())
    AssertionAssociationTypes.assert_code_matches(response_data, association_type1['code'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "en_US",
                                                              payload['translations']['en_US']['name'])


@pytest.mark.smoke
@pytest.mark.regression
def test_TC365_agregar_traduccion_nueva_en_es_ES_exitoso(setup_teardown_association_types):
    headers, association_type1, _ = setup_teardown_association_types
    headers_general = build_auth_headers(headers.copy())
    url = EndpointAssociationTypes.code(association_type1['code'])
    en_us_id = association_type1["translations"]["en_US"]["@id"]
    payload = generate_association_type_translations_data(
        langs=["en_US", "es_ES"],
        overrides={"en_US": {"@id": en_us_id}}
    )
    response = SyliusRequest.put(url, headers_general, payload)
    response_data = response.json()
    log_request_response(url, response, headers_general, payload)

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_type_edit_output_schema(response.json())
    AssertionAssociationTypes.assert_code_matches(response_data, association_type1['code'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "en_US",
                                                              payload['translations']['en_US']['name'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "es_ES",
                                                              payload['translations']['es_ES']['name'])
