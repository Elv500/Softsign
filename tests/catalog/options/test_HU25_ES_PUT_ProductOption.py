import pytest
from faker import Faker
fake = Faker()

from src.assertions.options_assertions import AssertionOptions
from src.assertions.status_code_assertions import AssertionStatusCode
from src.data.options import generate_options_source_data, generate_updated_options_payload, \
    generate_options_source_data_with_values, generate_updated_options_payload_with_values
from src.routes.endpoint_options import EndpointOptions
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response


#Este test verifica que una opción existente se actualiza correctamente.
@pytest.mark.functional
@pytest.mark.smoke
def test_tc311_Verificar_que_una_opción_existente_se_actualiza_correctamente(setup_options_cleanup):
    headers, add_option_for_cleanup = setup_options_cleanup
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    add_option_for_cleanup(code)
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload(code, translation_id)
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionOptions.assert_options_put_output_schema(response.json())

#Este test verifica que al intentar actualizar una opción con un código inexistente, se recibe un error 404.
@pytest.mark.functional
@pytest.mark.negative
def test_tc312_Verificar_error_al_actualizar_opción_con_codigo_inexistente(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    code = "test_code_inexistente"
    updated_payload = generate_updated_options_payload(code, "test_translation_id_inexistente")
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_404(response)

#Este test verificar que al intentar actualizar una opcion con un code vacío se recibe un error 404
@pytest.mark.functional
@pytest.mark.negative
def test_tc313_Verificar_error_al_actualizar_opción_con_code_vacío(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    code = ""
    updated_payload = generate_updated_options_payload(code, "test_translation_id_inexistente")
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_404(response)

#Este test verifica que no se pueda actualizar una opcion sun el campo obligatorio "name" en el payload.
@pytest.mark.functional
@pytest.mark.negative
def test_tc314_Verificar_error_al_actualizar_opción_sin_el_campo_obligatorio_nombre(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload(code, translation_id)
    updated_payload["translations"]["en_US"]["name"] = ""
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_422(response)

#Este test verifica que al actualizar una opcion con un name con menos de 2 caracteres se recibe un error 422.
@pytest.mark.functional
@pytest.mark.negative
def test_tc318_Verificar_error_al_actualizar_opción_con_nombre_menor_a_2_caracteres(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload(code, translation_id)
    updated_payload["translations"]["en_US"]["name"] = fake.pystr(min_chars=1, max_chars=1)
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_422(response)

#Este test verifica que al actualizar una opción con un name con más de 255 caracteres se recibe un error 422.
@pytest.mark.functional
@pytest.mark.negative
def test_tc319_Verificar_error_al_actualizar_opción_con_nombre_mayor_a_255_caracteres(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload(code, translation_id)
    updated_payload["translations"]["en_US"]["name"] = fake.pystr(min_chars=256, max_chars=300)
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_422(response)

#Este test verifica que al actualizar una opción con position de tipo string se recibe un error 400.
@pytest.mark.functional
@pytest.mark.negative
def test_tc320_Verificar_error_al_actualizar_opción_con_position_de_tipo_string(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload(code, translation_id)
    updated_payload["position"] = fake.word()
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_400(response)

#Este test verifica que al actualizar una opción con position de tipo decimal se recibe un error 400.
@pytest.mark.functional
@pytest.mark.negative
def test_tc321_Verificar_error_al_actualizar_opción_con_position_de_tipo_decimal(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload(code, translation_id)
    updated_payload["position"] = round(fake.random.uniform(1.0, 100.0), 2)
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_400(response)

#Este test verifica que al actualizar una opción con position de tipo negativo se recibe un error 400.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.xfail(reason="Known issue BUG: Validación faltante para valores negativos en campo 'position' - Comportamiento inconsistente al normalizar", run=True)
def test_tc322_Verificar_error_al_actualizar_opción_con_position_de_tipo_negativo(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload(code, translation_id)
    updated_payload["position"] = fake.random_int(min=-1000, max=-1)
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_400(response)

#Este test verifica que al actualizar una opción con un position mayor a 999999999 se recibe un error 400/422.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.xfail(reason="Known issue BUG: Normalización inconsistente al actualizar 'position' con valores >999,999,999 - Sin validación y comportamiento impredecible", run=True)
def test_tc323_Verificar_error_al_actualizar_opción_con_position_mayor_a_9999999999(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload(code, translation_id)
    updated_payload["position"] = fake.random_int(min=10000000000, max=100000000000)
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_400(response)


#Este test verifica error al intentar actualizar una opción sin autenticación.
@pytest.mark.functional
@pytest.mark.negative
def test_tc324_Verificar_error_al_intentar_actualizar_opción_sin_autenticación():
    code = "test_code_inexistente"
    updated_payload = generate_updated_options_payload(code, "test_translation_id_inexistente")
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), {}, updated_payload)
    log_request_response(EndpointOptions.code(code), response, {}, updated_payload)
    AssertionStatusCode.assert_status_code_401(response)
    assert response.json()["message"] == "JWT Token not found"

#Este test verifica error al intentar actualizar una opción con token inválido.
@pytest.mark.functional
@pytest.mark.negative
def test_tc325_Verificar_error_al_intentar_actualizar_opción_con_token_inválido():
    code = "test_code_inexistente"
    updated_payload = generate_updated_options_payload(code, "test_translation_id_inexistente")
    headers = {"Authorization": "Bearer invalid_token"}
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_401(response)
    assert response.json()["message"] == "Invalid JWT Token"

#Este test verifica error al intentar actualizar una opción con un idioma no soportado.
@pytest.mark.functional
@pytest.mark.negative
def test_tc326_Verificar_error_al_intentar_actualizar_opción_con_idioma_no_soportado(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload(code, translation_id)
    updated_payload["translations"]["xx_XX"] = {"name": fake.word().capitalize()}
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_422(response)

#Este test verifica que se pueda actualizar una opción con values
@pytest.mark.functional
@pytest.mark.smoke
def test_tc327_Verificar_que_se_puede_actualizar_opción_con_values(setup_options_cleanup):
    headers, add_option_for_cleanup = setup_options_cleanup
    payload = generate_options_source_data_with_values()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionOptions.assert_options_add_output_schema(response.json())
    code = response.json()["code"]
    add_option_for_cleanup(code)
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload_with_values(code, response.json().get("values", []), translation_id)
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionOptions.assert_options_put_output_schema(response.json())

#Este test verifica que al intentar actualizar una opción con values sin el campo obligatorio “English (United States)”
@pytest.mark.functional
@pytest.mark.negative
def test_tc328_Verificar_error_al_intentar_actualizar_opción_con_values_sin_campo_obligatorio_English_US(setup_options_cleanup):
    headers, add_option_for_cleanup = setup_options_cleanup
    payload = generate_options_source_data_with_values()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    log_request_response(EndpointOptions.options(), response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionOptions.assert_options_add_output_schema(response.json())
    code = response.json()["code"]
    en_us_translation = response.json()["translations"].get("en_US", {})
    translation_id = en_us_translation.get("@id")
    updated_payload = generate_updated_options_payload_with_values(code, payload.get("values", []), translation_id)
    for value in updated_payload.get("values", []):
        if "en_US" in value.get("translations", {}):
            value["translations"]["en_US"]["value"] = ""
    response = SyliusRequest().put_with_custom_headers(EndpointOptions.code(code), headers, updated_payload)
    log_request_response(EndpointOptions.code(code), response, headers, updated_payload)
    AssertionStatusCode.assert_status_code_422(response)