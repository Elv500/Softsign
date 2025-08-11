import logging
import pytest
import time

from src.assertions.customergroup_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from src.data.customer_group import generate_customer_group_source_data
from utils.logger_helpers import log_request_response

logger = logging.getLogger(__name__)


# Admin > Customer - Group > TC_293 Eliminar grupo de clientes existente
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
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
@pytest.mark.regression
def test_TC294_eliminar_grupo_codigo_inexistente(auth_headers):
    
    codigo_inexistente = "grupo_inexistente_12345"
    endpoint = EndpointCustomerGroup.code(codigo_inexistente)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(response)


# Admin > Customer - Group > TC_295 Verificar que no permita eliminar grupo sin token de autenticación
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
def test_TC295_eliminar_grupo_sin_token():
    
    codigo_existente = "retail"
    endpoint = EndpointCustomerGroup.code(codigo_existente)
    response = SyliusRequest.delete(endpoint, {})
    
    log_request_response(endpoint, response, headers={})
    
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_296 Verificar que no permita eliminar grupo con token inválido
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
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
@pytest.mark.regression
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
    assert elapsed < 3.0


# Admin > Customer - Group > TC_298 Verificar headers de respuesta al eliminar
@pytest.mark.functional
@pytest.mark.regression
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
    
    # c verificar que no hay content-type ya que es 204 No Content
    assert response.content == b"" or len(response.content) == 0


# Admin > Customer - Group > TC_299 Verificar que el grupo eliminado no exista más
@pytest.mark.functional
@pytest.mark.regression
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


# Admin > Customer - Group > TC_300 Verificar que no permita eliminar el mismo grupo dos veces
@pytest.mark.negative
@pytest.mark.regression
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


# Admin > Customer - Group > TC_301 Verificar eliminación de grupo con caracteres especiales en el nombre
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.regression
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
@pytest.mark.regression
def test_TC302_eliminar_grupo_codigo_muy_largo(auth_headers):
    
    codigo_muy_largo = "a" * 260 #el limite es 255
    endpoint = EndpointCustomerGroup.code(codigo_muy_largo)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(response)


# Admin > Customer - Group > TC_303 Verificar que no permita eliminar grupo con código vacío
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC303_eliminar_grupo_codigo_vacio(auth_headers):
    
    codigo_vacio = ""
    endpoint = EndpointCustomerGroup.code(codigo_vacio)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(response)


# Admin > Customer - Group > TC_304 Verificar eliminación concurrente del mismo grupo
@pytest.mark.negative
@pytest.mark.stress
@pytest.mark.regression
def test_TC304_eliminacion_concurrente_mismo_grupo(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    
    import threading
    import time
    
    results = []
    
    def delete_group():
        try:
            response = SyliusRequest.delete(endpoint, auth_headers)
            results.append(response.status_code)
        except Exception as e:
            results.append(str(e))
    
    thread1 = threading.Thread(target=delete_group)
    thread2 = threading.Thread(target=delete_group)
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    assert 204 in results
    assert 404 in results or len([r for r in results if r == 204]) == 1


# Admin > Customer - Group > TC_305 Verificar eliminación de grupo con diferentes métodos HTTP incorrectos
@pytest.mark.negative
@pytest.mark.regression
def test_TC305_eliminar_grupo_metodos_http_incorrectos(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    
    import requests
    post_response = requests.post(endpoint, headers=auth_headers)
    log_request_response(endpoint, post_response, headers=auth_headers)
    
    put_response = requests.put(endpoint, headers=auth_headers, json={})
    log_request_response(endpoint, put_response, headers=auth_headers)
    assert put_response.status_code != 204
    
    delete_response = SyliusRequest.delete(endpoint, auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)


# Admin > Customer - Group > TC_306 Verificar que no se pueda eliminar grupo del sistema (retail)
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
def test_TC306_no_eliminar_grupo_sistema(auth_headers):
    
    codigo_sistema = "retail"
    endpoint = EndpointCustomerGroup.code(codigo_sistema)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_307 Verificar eliminación de múltiples grupos secuencialmente
@pytest.mark.functional
@pytest.mark.stress
@pytest.mark.regression
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
@pytest.mark.regression
def test_TC308_eliminar_grupo_codigo_unicode(auth_headers):
    
    codigo_unicode = "grupo_测试_ñáéíóú"
    endpoint = EndpointCustomerGroup.code(codigo_unicode)
    response = SyliusRequest.delete(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(response)


# Admin > Customer - Group > TC_309 Verificar eliminación con Content-Type incorrecto (no debería afectar DELETE)
@pytest.mark.functional
@pytest.mark.regression
def test_TC309_eliminar_grupo_content_type_incorrecto(auth_headers):
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    
    import requests
    headers_with_text = auth_headers.copy()
    headers_with_text['Content-Type'] = 'text/plain'
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = requests.delete(endpoint, headers=headers_with_text)
    
    log_request_response(endpoint, response, headers=headers_with_text)
    
    AssertionStatusCode.assert_status_code_204(response)


# Admin > Customer - Group > TC_310 Verificar que eliminación no afecte otros recursos
@pytest.mark.functional
@pytest.mark.regression
def test_TC310_eliminar_grupo_no_afecta_otros_recursos(auth_headers):
    
    data1 = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    response1 = SyliusRequest.post(create_endpoint, auth_headers, data1)
    AssertionStatusCode.assert_status_code_201(response1)
    code1 = response1.json()["code"]
    
    data2 = generate_customer_group_source_data()
    response2 = SyliusRequest.post(create_endpoint, auth_headers, data2)
    AssertionStatusCode.assert_status_code_201(response2)
    code2 = response2.json()["code"]
    
    delete_endpoint = EndpointCustomerGroup.code(code1)
    delete_response = SyliusRequest.delete(delete_endpoint, auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)
    
    get_endpoint = EndpointCustomerGroup.code(code2)
    get_response = SyliusRequest.get(get_endpoint, auth_headers)
    
    log_request_response(get_endpoint, get_response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(get_response)
    assert get_response.json()["code"] == code2
    
    SyliusRequest.delete(EndpointCustomerGroup.code(code2), auth_headers)
