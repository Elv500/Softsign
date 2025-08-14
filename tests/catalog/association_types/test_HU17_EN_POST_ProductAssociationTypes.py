import pytest

from src.assertions.association_types_assertions import AssertionAssociationTypes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_product_association import EndpointAssociationTypes
from src.routes.request import SyliusRequest
from src.data.association_types import generate_association_types_source_data


# Catálogo > Association Types - TC_120 Crear tipo de asociación con code y translations.en_US.name válidos [Exitoso]
@pytest.mark.smoke
@pytest.mark.regression
def test_TC120_crear_tipo_asociacion_code_y_translations_en_US_name_validos_exitoso(teardown_association_types):
    headers, created_inventories = teardown_association_types
    payload = generate_association_types_source_data()
    url = EndpointAssociationTypes.association_types()
    AssertionAssociationTypes.assert_association_type_add_input_schema(payload)

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_201(response)
    AssertionAssociationTypes.assert_association_type_add_output_schema(response.json())
    AssertionAssociationTypes.assert_code_matches(response_data, payload['code'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "en_US",
                                                              payload['translations']['en_US']['name'])
    created_inventories.append(payload['code'])


# Catálogo > Association Types - TC_121 Crear tipo de asociación con múltiples traducciones válidas (en_US, es_ES) [Exitoso]
@pytest.mark.smoke
@pytest.mark.regression
def test_TC121_crear_tipo_asociacion_multiples_traducciones_validas_en_US_es_ES_exitoso(teardown_association_types):
    headers, created_inventories = teardown_association_types
    payload = generate_association_types_source_data(include_es_ES=True, include_es_MX=True)
    url = EndpointAssociationTypes.association_types()
    AssertionAssociationTypes.assert_association_type_add_input_schema(payload)

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()

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


# Catálogo > Association Types - TC_122 Validar creación con code de 2 caracteres [Exitoso]
@pytest.mark.functional
@pytest.mark.regression
def test_TC122_validar_creacion_code_2_caracteres_exitoso(teardown_association_types):
    headers, created_inventories = teardown_association_types
    payload = generate_association_types_source_data(code="ab")
    url = EndpointAssociationTypes.association_types()
    AssertionAssociationTypes.assert_association_type_add_input_schema(payload)

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_201(response)
    AssertionAssociationTypes.assert_association_type_add_output_schema(response.json())
    AssertionAssociationTypes.assert_code_matches(response_data, payload['code'])
    created_inventories.append(payload['code'])


# Catálogo > Association Types - TC_123 Validar creación con code de 255 caracteres [Exitoso]
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

    AssertionStatusCode.assert_status_code_201(response)
    AssertionAssociationTypes.assert_association_type_add_output_schema(response_data)
    AssertionAssociationTypes.assert_code_matches(response_data, payload['code'])
    created_inventories.append(payload['code'])


# Catálogo > Association Types - TC_124 Validar error si code tiene solo 1 caracter
@pytest.mark.regression
@pytest.mark.negative
def test_TC124_validar_error_code_1_caracter(auth_headers):
    headers = auth_headers
    payload = generate_association_types_source_data(code="a")
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)
    AssertionAssociationTypes.assert_violation_message(response_data,
                                                       "Association type code must be at least 2 characters long.")


# Catálogo > Association Types - TC_125 Validar error si code supera los 255 caracteres
@pytest.mark.regression
@pytest.mark.negative
def test_TC125_validar_error_code_supera_255_caracteres(auth_headers):
    headers = auth_headers
    code_256_chars = "a" * 256
    payload = generate_association_types_source_data(code=code_256_chars)
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)
    AssertionAssociationTypes.assert_violation_message(response_data,
                                                       "Association type code must not be longer than 255 characters.")


# Catálogo > Association Types - TC_126 Validar error si code contiene caracteres inválidos (ej. @@??)
@pytest.mark.regression
@pytest.mark.negative
def test_TC126_validar_error_code_caracteres_invalidos(auth_headers):
    headers = auth_headers
    payload = generate_association_types_source_data(code=123)
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)

    AssertionStatusCode.assert_status_code_400(response)


# Catálogo > Association Types - TC_127 Validar error si code ya existe en el sistema
@pytest.mark.regression
@pytest.mark.negative
def test_TC127_validar_error_code_ya_existe(teardown_association_types):
    headers, created_inventories = teardown_association_types
    payload = generate_association_types_source_data()
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    created_inventories.append(payload['code'])

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)
    AssertionAssociationTypes.assert_violation_message(response_data,
                                                       "The association type with given code already exists.")


# Catálogo > Association Types - TC_128 Validar error si falta el campo code
@pytest.mark.regression
@pytest.mark.negative
def test_TC128_validar_error_falta_campo_code(auth_headers):
    headers = auth_headers
    payload = generate_association_types_source_data()
    del payload['code']
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)
    AssertionAssociationTypes.assert_violation_message(response_data,
                                                       "Please enter association type code.")


# Catálogo > Association Types - TC_129 Validar error si falta el campo translations
@pytest.mark.regression
@pytest.mark.negative
def test_TC129_validar_error_falta_campo_translations(auth_headers):
    headers = auth_headers
    payload = generate_association_types_source_data()
    del payload['translations']
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)
    AssertionAssociationTypes.assert_violation_message(response_data,
                                                       "Please enter association type name.")


# Catálogo > Association Types - TC_130 Validar error si translations está vacío
@pytest.mark.regression
@pytest.mark.negative
def test_TC130_validar_error_translations_vacio(auth_headers):
    headers = auth_headers
    payload = generate_association_types_source_data(en_US_name="")
    payload['translations'] = {"en_US": {"name": ""}}
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_422(response)
    AssertionAssociationTypes.assert_association_type_add_error_schema(response_data)
    AssertionAssociationTypes.assert_violation_message(response_data,
                                                       "Please enter association type name.")


# Catálogo > Association Types - TC_131 Crear tipo de asociación con solo una traducción (en_US) [Exitoso]
@pytest.mark.regression
def test_TC131_crear_tipo_asociacion_solo_una_traduccion_en_US_exitoso(teardown_association_types):
    headers, created_inventories = teardown_association_types
    payload = generate_association_types_source_data(en_US_name="prueba")
    url = EndpointAssociationTypes.association_types()
    AssertionAssociationTypes.assert_association_type_add_input_schema(payload)

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_201(response)
    AssertionAssociationTypes.assert_association_type_add_output_schema(response.json())
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "en_US",
                                                              payload['translations']['en_US']['name'])
    created_inventories.append(payload['code'])


# Catálogo > Association Types - TC_132 Enviar solicitud sin token de autenticación
@pytest.mark.regression
@pytest.mark.security
@pytest.mark.negative
def test_TC132_enviar_solicitud_sin_token_autenticacion():
    headers = {}
    payload = generate_association_types_source_data()
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)

    AssertionStatusCode.assert_status_code_401(response)


# Catálogo > Association Types - TC_133 Enviar solicitud con token inválido
@pytest.mark.regression
@pytest.mark.security
@pytest.mark.negative
def test_TC133_enviar_solicitud_token_invalido():
    headers = {
        "Authorization": "Bearer invalid_token_123456789",
        "Content-Type": "application/json"
    }
    payload = generate_association_types_source_data()
    url = EndpointAssociationTypes.association_types()

    response = SyliusRequest.post(url, headers, payload)

    AssertionStatusCode.assert_status_code_401(response)
