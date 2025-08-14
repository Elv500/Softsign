import pytest

from src.assertions.association_types_assertions import AssertionAssociationTypes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_product_association import EndpointAssociationTypes
from src.routes.request import SyliusRequest
from src.data.association_types import generate_association_type_translations_data, build_auth_headers
from utils.logger_helpers import log_request_response


# Catálogo > Association Types - TC_364 Modificar traducción existente en inglés (en_US), pasando el campo `@id` [Exitoso]
@pytest.mark.smoke
@pytest.mark.regression
def test_TC364_modificar_traduccion_existente_en_US_pasando_id_exitoso(setup_teardown_association_types):
    headers, association_type1, _ = setup_teardown_association_types
    headers_general = build_auth_headers(headers.copy())
    url = EndpointAssociationTypes.code(association_type1['code'])
    en_us_id = association_type1["translations"]["en_US"]["@id"]
    payload = generate_association_type_translations_data(
        langs=["en_US"],
        overrides={"en_US": {"@id": en_us_id}},
    )
    AssertionAssociationTypes.assert_association_type_edit_input_schema(payload)

    response = SyliusRequest.put(url, headers_general, payload)
    response_data = response.json()
    log_request_response(url, response, headers_general, payload)

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_type_edit_output_schema(response.json())
    AssertionAssociationTypes.assert_code_matches(response_data, association_type1['code'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "en_US",
                                                              payload['translations']['en_US']['name'])


# Catálogo > Association Types - TC_365 Agregar traducción nueva en español (es_ES) [Exitoso]
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
    AssertionAssociationTypes.assert_association_type_edit_input_schema(payload)

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


# Catálogo > Association Types - TC_366 Modificar simultáneamente traducciones en en_US y es_ES [Exitoso]
@pytest.mark.functional
@pytest.mark.regression
def test_TC366_modificar_simultaneamente_traducciones_en_US_y_es_ES_exitoso(setup_teardown_association_types):
    headers, association_type1, _ = setup_teardown_association_types
    headers_general = build_auth_headers(headers.copy())
    url = EndpointAssociationTypes.code(association_type1['code'])
    response = SyliusRequest.get(url, headers)
    association_type1 = response.json()
    en_us_id = association_type1["translations"]["en_US"]["@id"]
    es_es_id = association_type1["translations"]["es_ES"]["@id"]
    payload = generate_association_type_translations_data(
        langs=["en_US", "es_ES"],
        overrides={"en_US": {"@id": en_us_id}, "es_ES": {"@id": es_es_id}}
    )
    AssertionAssociationTypes.assert_association_type_edit_input_schema(payload)

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


# Catálogo > Association Types - TC_367 Intentar modificar el campo code en el body [Se ignora, el código no cambia]
@pytest.mark.functional
@pytest.mark.regression
def test_TC367_intentar_modificar_campo_code_en_body_se_ignora_no_cambia(setup_teardown_association_types):
    headers, association_type1, _ = setup_teardown_association_types
    headers_general = build_auth_headers(headers.copy())
    url = EndpointAssociationTypes.code(association_type1['code'])
    en_us_id = association_type1["translations"]["en_US"]["@id"]
    payload = generate_association_type_translations_data(
        langs=["en_US"],
        overrides={"en_US": {"@id": en_us_id}},
        extra_fields={"code": "new-code"}
    )

    response = SyliusRequest.put(url, headers_general, payload)
    response_data = response.json()
    log_request_response(url, response, headers_general, payload)

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_type_edit_output_schema(response.json())
    AssertionAssociationTypes.assert_code_matches(response_data, association_type1['code'])


# Catálogo > Association Types - TC_368 Enviar body sin campo translations (se ignora el cambio)
@pytest.mark.functional
@pytest.mark.regression
def test_TC368_enviar_body_sin_campo_translations_se_ignora_el_cambio(setup_teardown_association_types):
    headers, association_type1, _ = setup_teardown_association_types
    headers_general = build_auth_headers(headers.copy())
    url = EndpointAssociationTypes.code(association_type1['code'])
    response = SyliusRequest.get(url, headers)
    association_type1 = response.json()
    en_us_id = association_type1["translations"]["en_US"]["@id"]
    payload = generate_association_type_translations_data(
        langs=["en_US", "es_ES"],
        overrides={"en_US": {"@id": en_us_id}}, extra_fields={"code": "new-code-ignored"}
    )

    response = SyliusRequest.put(url, headers_general, payload)
    response_data = response.json()
    log_request_response(url, response, headers_general, payload)

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_type_edit_output_schema(response_data)
    AssertionAssociationTypes.assert_code_matches(response_data, association_type1['code'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "en_US",
                                                              association_type1['translations']['en_US']['name'])


# Catálogo > Association Types - TC_369 Modificar traducción existente sin pasar @id
@pytest.mark.functional
@pytest.mark.regression
def test_TC369_modificar_traduccion_existente_sin_pasar_id(setup_teardown_association_types):
    headers, association_type1, _ = setup_teardown_association_types
    headers_general = build_auth_headers(headers.copy())
    url = EndpointAssociationTypes.code(association_type1['code'])
    payload = generate_association_type_translations_data(
        langs=["en_US"],
        overrides={"en_US": {"name": "nuevo-nombre-sin-id"}}
    )

    response = SyliusRequest.put(url, headers_general, payload)
    response_data = response.json()
    log_request_response(url, response, headers_general, payload)

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)


@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.regression
def test_TC370_modificar_recurso_con_code_inexistente(setup_teardown_association_types):
    headers, association_type1, _ = setup_teardown_association_types
    headers_general = build_auth_headers(headers.copy())
    url = EndpointAssociationTypes.code("xyz-abc-123")
    en_us_id = association_type1["translations"]["en_US"]["@id"]
    payload = generate_association_type_translations_data(
        langs=["en_US"],
        overrides={"en_US": {"@id": en_us_id}},
    )

    response = SyliusRequest.put(url, headers_general, payload)
    response_data = response.json()
    log_request_response(url, response, headers_general, payload)

    AssertionStatusCode.assert_status_code_404(response)
    AssertionAssociationTypes.assert_error_schema(response_data)


@pytest.mark.regression
@pytest.mark.security
@pytest.mark.functional
@pytest.mark.negative
def test_TC371_enviar_solicitud_con_token_invalido(setup_teardown_association_types):
    headers, association_type1, _ = setup_teardown_association_types
    headers_general = build_auth_headers(headers.copy())
    headers_general["Authorization"] = "Bearer invalid_token_123456789"

    url = EndpointAssociationTypes.code(association_type1['code'])
    en_us_id = association_type1["translations"]["en_US"]["@id"]
    payload = generate_association_type_translations_data(
        langs=["en_US"],
        overrides={"en_US": {"@id": en_us_id}},
    )

    response = SyliusRequest.put(url, headers_general, payload)
    response_data = response.json()
    log_request_response(url, response, headers_general, payload)

    AssertionStatusCode.assert_status_code_401(response)
    AssertionAssociationTypes.assert_invalid_jwt_error(response_data)

@pytest.mark.regression
@pytest.mark.functional
def test_TC372_validar_que_campos_no_modificados_permanecen_igual_exitoso(setup_teardown_association_types):
    headers, association_type1, _ = setup_teardown_association_types
    headers_general = build_auth_headers(headers.copy())
    url = EndpointAssociationTypes.code(association_type1['code'])
    response = SyliusRequest.get(url, headers)
    association_type1 = response.json()
    en_us_id = association_type1["translations"]["en_US"]["@id"]
    payload = generate_association_type_translations_data(
        langs=["en_US"],
        overrides={"en_US": {"@id": en_us_id}},
    )

    response = SyliusRequest.put(url, headers_general, payload)
    response_data = response.json()
    log_request_response(url, response, headers_general, payload)

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_type_edit_output_schema(response_data)
    AssertionAssociationTypes.assert_code_matches(response_data, association_type1['code'])

