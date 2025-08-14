import pytest
from faker import Faker
fake = Faker()

from src.assertions.options_assertions import AssertionOptions
from src.assertions.status_code_assertions import AssertionStatusCode
from src.data.options import generate_options_source_data, generate_options_source_data_with_values
from src.routes.endpoint_options import EndpointOptions
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response


#Validar que se puede crear una nueva opción de producto cuando se proporcionan datos válidos y el endpoint devuelva un codigo 201 indicando que la opción fue creada correctamente.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC108_Verificar_creacion_de_opción_exitosamente_con_datos_válidos(setup_add_options):
    headers, created_options = setup_add_options
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionOptions.assert_options_add_output_schema(response.json())
    created_options.append(response.json())

#Validar que no se puede crear una nueva opción de producto cuando no se proporcionan datos obligatorios y el endpoint devuelva un codigo 422 indicando que la opción no fue creada  que hubo un error.
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.negative
def test_TC109_Verificar_error_422_al_crear_opcion_sin_campos_obligatorios(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["code"] = ""
    payload["translations"]["en_US"]["name"] = ""
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    expected_messages = {
        "Please enter option code.",
        "Please enter option name.",
        "Option name must be at least 2 characters long."
    }
    actual_messages = {violation["message"] for violation in response.json()["violations"]}
    assert actual_messages == expected_messages

#Validar que no se puede crear una nueva opción de producto cuando no se proporcionan el campo transalations y el endpoint devuelva un codigo 422 indicando que la opción no fue creada que hubo un error.
@pytest.mark.functional
@pytest.mark.negative
def test_TC110_Verificar_error_422_al_crear_opcion_sin_el_campo_obligatorio_code(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["code"]= ""
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    # validacion del mensaje de error
    assert response.json()["detail"] == "code: Please enter option code."

#Validar que no se puede crear una nueva opción de producto cuando no se proporcionan el campo name y el endpoint devuelva un codigo 422 indicando que la opción no fue creada que hubo un error.
@pytest.mark.functional
@pytest.mark.negative
def test_TC111_Verificar_error_422_al_crear_opcion_sin_el_campo_obligatorio_name(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["translations"]["en_US"]["name"] = ""
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    expected_details = {
        "translations[en_US].name: Please enter option name.",
        "translations[en_US].name: Option name must be at least 2 characters long."
    }
    actual_details = set(response.json()["detail"].split("\n"))
    assert actual_details == expected_details

#Validar que no se puede crear una nueva opción de producto cuando se proporciona un código ya existente y el endpoint devuelva un codigo 422 indicando que la opción no fue creada porque hubo un error.
@pytest.mark.functional
@pytest.mark.negative
def test_TC112_Verificar_error_422_al_crear_opcion_con_codigo_existente(setup_add_options):
    headers, created_options = setup_add_options
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    created_options.append(response.json())
    # Intentar crear la misma opción nuevamente
    response_duplicate = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response_duplicate, headers, payload)
    AssertionStatusCode.assert_status_code_422(response_duplicate)
    assert response_duplicate.json()["detail"] == "code: The option with given code already exists."

#Validar que no se puede crear una nueva opción de producto cuando se proporciona un código con espacios y el endpoint devuelva un codigo 422 indicando que la opción no fue creada porque hubo un error.
@pytest.mark.functional
@pytest.mark.negative
def test_TC113_Verificar_error_al_crear_opcion_con_code_con_espacios(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["code"] = fake.sentence()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    assert response.json()["detail"] == "code: Option code can only be comprised of letters, numbers, dashes and underscores."

#Validar que no se puede crear una nueva opción de producto cuando se proporciona un código con más de 255 caracteres y el endpoint devuelva un codigo 422 indicando que la opción no fue creada porque hubo un error.
@pytest.mark.functional
@pytest.mark.boundary
def test_TC222_Verificar_que_el_campo_code_acepte_maximo_255_caracteres(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["code"] = fake.pystr(min_chars=256, max_chars=300)
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    assert response.json()["detail"] == "code: The code must not be longer than 255 characters."

#Validar que no se puede crear una nueva opción de producto cuando se proporciona un código con menos de 2 caracteres y el endpoint devuelva un codigo 422 indicando que la opción no fue creada porque hubo un error.
@pytest.mark.functional
@pytest.mark.boundary
def test_TC223_Verificar_error_al_crear_option_name_con_menos_de_2_caracteres(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["translations"]["en_US"]["name"] = fake.pystr(min_chars=1, max_chars=1)
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    assert response.json()["detail"] == "translations[en_US].name: Option name must be at least 2 characters long."

#Validar que no se puede crear una nueva opción de producto cuando se proporciona un código con más de 255 caracteres y el endpoint devuelva un codigo 422 indicando que la opción no fue creada porque hubo un error.
@pytest.mark.functional
@pytest.mark.boundary
def test_TC224_Verificar_error_al_crear_option_name_con_mas_de_255_caracteres(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["translations"]["en_US"]["name"] = fake.pystr(min_chars=256, max_chars=300)
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    assert response.json()["detail"] == "translations[en_US].name: Option name must not be longer than 255 characters."

#Validar que no se puede crear una nueva opción de producto cuando se proporciona un valor no entero en el campo position y el endpoint devuelva un codigo 400 que indica que ocurrió un error.
@pytest.mark.functional
@pytest.mark.negative
def test_TC225_Verificar_error_al_crear_un_position_que_no_sea_entero(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["position"] = fake.word()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    assert response.json()["detail"] == "The type of the \"position\" attribute must be \"int\", \"string\" given."

#Validar que no se puede crear una nueva opción de producto cuando se proporciona un valor negativo en el campo position y el endpoint devuelva un codigo 422 indicando que la opción no fue creada porque hubo un error.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.xfail(reason="Known issue BUG: Validación faltante para valores negativos en campo 'position' - Comportamiento inconsistente al normalizar", run=True)
def test_TC226_Verificar_error_al_crear_opcion_con_position_negativo(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["position"] = fake.random_int(min=-1000, max=-1)
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionOptions.assert_options_add_output_schema(response.json())

#Validar que no se puede crear una nueva opción de producto cuando se proporciona un valor mayor a 999999999 en el campo position y el endpoint devuelva un codigo 422 indicando que hubo un error al crear la opcion.
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.xfail(reason="Known issue BUG: Error 500 (Internal Server Error) inapropiado al validar campo numérico", run=True)
def test_TC227_Verificar_error_al_crear_opcion_con_position_mayor_a_999999999(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["position"] = fake.random_int(min=1000000000, max=10000000000)
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)

#Validar que no se puede crear una nueva opción de producto sin autenticación y el endpoint devuelva un codigo 401 indicando que la opción no fue creada porque hubo un error.
@pytest.mark.smoke
@pytest.mark.negative
def test_TC228_Verificar_creacion_de_opcion_sin_autenticacion():
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers=None, payload=payload)
    log_request_response(EndpointOptions.options(), response, headers=None, payload=payload)
    AssertionStatusCode.assert_status_code_401(response)
    assert response.json()["message"] == "JWT Token not found"

#Validar que no se puede crear una nueva opción de producto con un token inválido y el endpoint devuelva un codigo 401 indicando que la opción no fue creada porque hubo un error.
@pytest.mark.negative
def test_TC229_Verificar_creacion_de_opcion_con_token_invalido():
    payload = generate_options_source_data()
    invalid_auth_headers = {
        "Authorization": "Bearer invalid_token",
        "Content-Type": "application/json"
    }
    response = SyliusRequest.post(EndpointOptions.options(), invalid_auth_headers, payload)
    log_request_response(EndpointOptions.options(), response, invalid_auth_headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    assert response.json()["message"] == "Invalid JWT Token"

#Validar que no se puede crear una nueva opción de producto cuando se proporciona un idioma no soportado y el endpoint devuelva un codigo 400 indicando que la opción no fue creada porque hubo un error.
@pytest.mark.negative
def test_TC230_Verificar_creacion_de_opcion_con_idioma_no_soportado(setup_add_options):
    headers, _ = setup_add_options
    payload = generate_options_source_data()
    payload["translations"]["xx_XX"] = {"name": "Test Option in Unsupported Language"}
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)

#Validar que se puede crear una nueva opción de producto con valores y el endpoint devuelva un codigo 201 indicando que la opción fue creada correctamente.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC231_Verificar_creacion_de_opcion_con_values(setup_add_options):
    headers, created_options = setup_add_options
    payload = generate_options_source_data_with_values()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionOptions.assert_options_add_output_schema(response.json())
    created_options.append(response.json())

