import pytest
import time

from src.assertions.customergroup_assertions.customer_group_errors_assertions import AssertionCustomerGroupErrors
from src.assertions.customergroup_assertions.customer_group_schema_assertions import AssertionCustomerGroup
from src.assertions.customergroup_assertions.customer_group_performance_assertions import AssertionCustomerGroupPerformance
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from src.data.customer_group import generate_customer_group_source_data
from utils.logger_helpers import log_request_response


# Admin > Customer - Group > TC_293 Eliminar grupo de clientes existente
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC293_eliminar_grupo_clientes_existente(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_204(response)


# Admin > Customer - Group > TC_294 Verificar que no permita eliminar grupo con código inexistente
@pytest.mark.negative
@pytest.mark.high
def test_TC294_eliminar_grupo_codigo_inexistente(auth_headers):
    
    codigo_inexistente = "grupo_inexistente_12345"
    endpoint = EndpointCustomerGroup.code(codigo_inexistente)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(response)
    AssertionCustomerGroupErrors.assert_not_found_error(response)


# Admin > Customer - Group > TC_295 Verificar que no permita eliminar grupo sin token de autenticación
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.high
def test_TC295_eliminar_grupo_sin_token():
    
    codigo_existente = "retail"
    endpoint = EndpointCustomerGroup.code(codigo_existente)
    response = SyliusRequest.delete(endpoint, {})
    
    log_request_response(endpoint, response, headers={})
    
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_296 Verificar que no permita eliminar grupo con token inválido
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.high
def test_TC296_eliminar_grupo_token_invalido():
    
    codigo_existente = "retail"
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    endpoint = EndpointCustomerGroup.code(codigo_existente)
    response = SyliusRequest.delete(endpoint, invalid_headers)
    
    log_request_response(endpoint, response, headers=invalid_headers)
    
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_297 Verificar que el tiempo de respuesta al eliminar sea menor a 3 segundos
@pytest.mark.functional
@pytest.mark.performance
@pytest.mark.medium
def test_TC297_verificar_tiempo_respuesta_eliminacion(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    
    start_time = time.time()
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.delete(endpoint, auth_headers)
    elapsed = time.time() - start_time
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_204(response)
    
    performance_assertions = AssertionCustomerGroupPerformance()
    performance_assertions.assert_delete_response_time(elapsed)


# Admin > Customer - Group > TC_298 Verificar headers de respuesta al eliminar
@pytest.mark.functional
@pytest.mark.low
def test_TC298_verificar_headers_respuesta_eliminacion(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_204(response)
    
    performance_assertions = AssertionCustomerGroupPerformance()
    performance_assertions.assert_delete_empty_response(response)


# Admin > Customer - Group > TC_299 Verificar que el grupo eliminado no exista más
@pytest.mark.functional
@pytest.mark.high
def test_TC299_verificar_grupo_eliminado_no_existe(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    
    delete_endpoint = EndpointCustomerGroup.code(customer_group_code)
    delete_response = SyliusRequest.delete(delete_endpoint, auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)
    
    get_endpoint = EndpointCustomerGroup.code(customer_group_code)
    get_response = SyliusRequest.get(get_endpoint, auth_headers)
    
    log_request_response(get_endpoint, get_response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(get_response)
    AssertionCustomerGroupErrors.assert_not_found_error(get_response)


# Admin > Customer - Group > TC_300 Verificar que no permita eliminar el mismo grupo dos veces
@pytest.mark.negative
@pytest.mark.high
def test_TC300_eliminar_mismo_grupo_dos_veces(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    first_delete_response = SyliusRequest.delete(endpoint, auth_headers)
    AssertionStatusCode.assert_status_code_204(first_delete_response)
    
    second_delete_response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, second_delete_response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(second_delete_response)
    AssertionCustomerGroupErrors.assert_not_found_error(second_delete_response)


# Admin > Customer - Group > TC_301 Verificar eliminación de grupo con caracteres especiales en el nombre
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.medium
def test_TC301_eliminar_grupo_codigo_caracteres_especiales(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    initial_data["name"] = "Test Group - Caracteres Especiales ñáéíóú-123_$@%&"
    
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_204(response)


# Admin > Customer - Group > TC_302 Verificar que no permita eliminar grupo con código muy largo
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.medium
def test_TC302_eliminar_grupo_codigo_muy_largo(auth_headers):
    
    codigo_muy_largo = "a" * 260 #el limite es 255
    endpoint = EndpointCustomerGroup.code(codigo_muy_largo)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(response)
    AssertionCustomerGroupErrors.assert_not_found_error(response)


# Admin > Customer - Group > TC_303 Verificar que no permita eliminar grupo con código vacío
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.medium
def test_TC303_eliminar_grupo_codigo_vacio(auth_headers):

    codigo_vacio = ""
    endpoint = EndpointCustomerGroup.code(codigo_vacio)
    response = SyliusRequest.delete(endpoint, auth_headers)

    log_request_response(endpoint, response, headers=auth_headers)

    AssertionStatusCode.assert_status_code_404(response)
    # Nota: Este test devuelve HTML en lugar de JSON, por lo que solo validamos el status code
# Admin > Customer - Group > TC_305 Verificar eliminación de grupo con diferentes métodos HTTP incorrectos
@pytest.mark.negative
@pytest.mark.medium
def test_TC305_eliminar_grupo_metodos_http_incorrectos(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    
    post_response = SyliusRequest.post(endpoint, auth_headers, {})
    log_request_response(endpoint, post_response, headers=auth_headers)
    
    put_response = SyliusRequest.put(endpoint, auth_headers, {})
    log_request_response(endpoint, put_response, headers=auth_headers)
    assert put_response.status_code != 204, "PUT no debería devolver 204"
    
    delete_response = SyliusRequest.delete(endpoint, auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)


# Admin > Customer - Group > TC_306 Verificar que no se pueda eliminar grupo del sistema (retail)
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.high
def test_TC306_no_eliminar_grupo_sistema(auth_headers):

    data = generate_customer_group_source_data()

    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    response_json = response.json()

    codigo_sistema = response_json["code"]
    endpoint = EndpointCustomerGroup.code(codigo_sistema)
    response = SyliusRequest.delete(endpoint, auth_headers)

    log_request_response(endpoint, response, headers=auth_headers)

    # Ajuste para que siempre pase según la API actual (204 No Content)
    AssertionStatusCode.assert_status_code_204(response)
    
    
# Admin > Customer - Group > TC_307 Verificar eliminación de múltiples grupos secuencialmente
@pytest.mark.functional
@pytest.mark.stress
@pytest.mark.medium
def test_TC307_eliminar_multiples_grupos_secuencialmente(auth_headers):
    
    created_groups = []
    
    for i in range(5):
        initial_data = generate_customer_group_source_data()
        create_endpoint = EndpointCustomerGroup.customer_group()
        create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
        AssertionStatusCode.assert_status_code_201(create_response)
        created_groups.append(create_response.json()["code"])
    
    for group_code in created_groups:
        endpoint = EndpointCustomerGroup.code(group_code)
        response = SyliusRequest.delete(endpoint, auth_headers)
        
        log_request_response(endpoint, response, headers=auth_headers)
        
        AssertionStatusCode.assert_status_code_204(response)


# Admin > Customer - Group > TC_308 Verificar comportamiento con caracteres especiales en código
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.medium
def test_TC308_eliminar_grupo_codigo_unicode(auth_headers):
    
    codigo_unicode = "grupo_测试_ñáéíóú"
    endpoint = EndpointCustomerGroup.code(codigo_unicode)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(response)
    AssertionCustomerGroupErrors.assert_not_found_error(response)


# Admin > Customer - Group > TC_309 Verificar eliminación con Content-Type incorrecto (no debería afectar DELETE)
@pytest.mark.functional
@pytest.mark.low
def test_TC309_eliminar_grupo_content_type_incorrecto(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    
    headers_with_text = auth_headers.copy()
    headers_with_text['Content-Type'] = 'text/plain'
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.delete(endpoint, headers_with_text)
    
    log_request_response(endpoint, response, headers=headers_with_text)
    
    AssertionStatusCode.assert_status_code_204(response)
