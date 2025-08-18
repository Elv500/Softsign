import pytest
from faker import Faker
fake = Faker()
import time

from src.assertions.status_code_assertions import AssertionStatusCode
from src.data.options import generate_options_source_data
from src.routes.endpoint_options import EndpointOptions
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response


#Este test verifica que una opción se elimina correctamente cuando se proporciona un código válido.
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_tc386_Verificar_eliminar_una_opcion_con_code_valido(auth_headers):
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), auth_headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    response = SyliusRequest().delete(EndpointOptions.code(code), auth_headers)
    log_request_response(EndpointOptions.code(code), response, auth_headers)
    AssertionStatusCode.assert_status_code_204(response)

#Este test verifica que la opcion eliminada desaparezca de la lista de opciones
@pytest.mark.functional
@pytest.mark.medium
def test_tc387_Verificar_opcion_eliminada_no_aparece_en_lista_de_opciones(auth_headers):
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), auth_headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    response = SyliusRequest().delete(EndpointOptions.code(code), auth_headers)
    AssertionStatusCode.assert_status_code_204(response)
    endpoint = EndpointOptions.code(code)
    response = SyliusRequest.get(EndpointOptions.code(code), auth_headers)
    log_request_response(endpoint, response, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)

#Este test verifica que al intentar eliminar una opción con un código inexistente, se recibe un error 404.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.high
def test_tc388_Verificar_error_al_eliminar_opcion_con_un_code_que_no_existe(auth_headers):
    code = fake.pystr(min_chars=8, max_chars=12)
    response = SyliusRequest().delete(EndpointOptions.code(code), auth_headers)
    log_request_response(EndpointOptions.code(code), response, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)

#Este test verifica que al intentar eliminar una opción con un code en formato incorrecto, se recibe un error 404.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.medium
def test_tc389_Verificar_error_al_eliminar_opcion_con_code_en_formato_incorrecto(auth_headers):
    code = fake.sentence()
    response = SyliusRequest().delete(EndpointOptions.code(code), auth_headers)
    log_request_response(EndpointOptions.code(code), response, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)

#Este test verifica que al intentar eliminar una opción con code vacio, se recibe un error 404.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.medium
def test_tc390_Verificar_error_al_eliminar_opcion_con_code_vacio(auth_headers):
    code = ""
    response = SyliusRequest().delete(EndpointOptions.code(code), auth_headers)
    log_request_response(EndpointOptions.code(code), response, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)

#Este test verifica que al intentar eliminar una opción que ya ha sido eliminada, se recibe un error 404.
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.medium
def test_tc391_Verificar_error_al_eliminar_opcion_ya_eliminada(auth_headers):
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), auth_headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]
    response = SyliusRequest().delete(EndpointOptions.code(code), auth_headers)
    AssertionStatusCode.assert_status_code_204(response)
    response = SyliusRequest().delete(EndpointOptions.code(code), auth_headers)
    log_request_response(EndpointOptions.code(code), response, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)

#Este test verifica que al intentar eliminar una opción sin autenticación, se recibe un error 401.
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.high
def test_tc392_Verificar_error_al_eliminar_opcion_sin_autenticacion():
    code = fake.pystr(min_chars=8, max_chars=12)
    response = SyliusRequest().delete(EndpointOptions.code(code), {})
    log_request_response(EndpointOptions.code(code), response, {})
    AssertionStatusCode.assert_status_code_401(response)
    assert response.json()["message"] == "JWT Token not found"

#Este test verifica que al intentar eliminar una opción con un token inválido, se recibe un error 401.
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.high
def test_tc393_Verificar_error_al_eliminar_opcion_con_token_invalido():
    code = fake.pystr(min_chars=8, max_chars=12)
    headers = {"Authorization": "Bearer invalid_token"}
    response = SyliusRequest().delete(EndpointOptions.code(code), headers)
    log_request_response(EndpointOptions.code(code), response, headers)
    AssertionStatusCode.assert_status_code_401(response)
    assert response.json()["message"] == "Invalid JWT Token"

#Este test verifica que al intentar eliminar una opción con un token expirado, se recibe un error 401.
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.high
def test_tc394_Verificar_error_al_eliminar_opcion_con_token_expirado():
    code = fake.pystr(min_chars=8, max_chars=12)
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTUxNTE5MDAsImV4cCI6MTc1NTE1NTUwMCwicm9sZXMiOlsiUk9MRV9BRE1JTklTVFJBVElPTl9BQ0NFU1MiLCJST0xFX0FQSV9BQ0NFU1MiXSwidXNlcm5hbWUiOiJhcGkifQ.PIh2JT4PVgURJ9qHZfKkmkc0PT93CynyVSWnrtck-Sk_JF_HCwo6qO1r9HmuVYje-QbLdhgdMiUv_yCv0Zcm7XnzqQICC7qQpstVC10A9rdjsUKqHtPMGHrDeIcVfHX-QDD8ulymtpiFFdDVuX3RhBi5rdVXAqiiicqYGsvG5Ass7xJBy41kHhJO8cEKvnZZiBqjGf9rDzyMb86yR6CRtd5MigxlWX3Ve4uvCbtH_RLPHF44Kej4mGtZQ2vgkEqgmVauA4jrZMUGEXcXYiUEUL0FLHAzCnlM4_6AIHaMLQDQOwpkS5IzfLZSEjz3tX5r5K_3VEd28RaHr2k2sCETtK6iIB9z3IJTMMCQiBBpoOS0vyrpEDCDMj3FblQG3Wn3C3Dj2Z6IhU7YWoMhChx2hZFBiZRSvEn8DpwLRnm3n7kGVnVyOWWo9YH9AE1GK0zHUThxLomFFEuWs_YLEZiAkkHopxZdr7mp1w4voZ3BxO6-7H7A0k_3GMY28EfM2ZfzeZUZZtLqZ91-NZIGGrKwuD_8JhH-CaG-KyVEwfseZpiKeInJJz9Nbypwfk7W9ReRSh8-M7vwy0MPNoz-6B5IqttwMTQkqw1HwTUg6oBbDxOSIpJQ9zbl4-1rwCznP3TzbFncqNowXJbjgprOPbxhQmw1n-iwXSxXXK9Dl8vhCKU"}
    response = SyliusRequest().delete(EndpointOptions.code(code), headers)
    log_request_response(EndpointOptions.code(code), response, headers)
    AssertionStatusCode.assert_status_code_401(response)
    assert response.json()["message"] == "Expired JWT Token"

#Este test verifica que al intentar eliminar una opción la respuesta no tarde más de 2 segundos.
@pytest.mark.performance
@pytest.mark.low
def test_tc395_Verificar_tiempo_respuesta_al_eliminar_opcion(setup_options_cleanup):
    headers, _ = setup_options_cleanup
    payload = generate_options_source_data()
    response = SyliusRequest.post(EndpointOptions.options(), headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    code = response.json()["code"]

    start_time = time.time()
    response = SyliusRequest().delete(EndpointOptions.code(code), headers)
    elapsed = time.time() - start_time

    log_request_response(EndpointOptions.code(code), response, headers)
    AssertionStatusCode.assert_status_code_204(response)
    assert elapsed <= 2, f"La respuesta tardó más de 2 segundos: {elapsed:.2f}s"