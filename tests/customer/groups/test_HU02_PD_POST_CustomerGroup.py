import logging
import pytest
import requests
import time

from src.assertions.customergroup_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from src.data.customer_group import generate_customer_group_source_data
from utils.logger_helpers import log_request_response

logger = logging.getLogger(__name__)

# Variable global para controlar delay entre tests
_last_request_time = 0

def safe_api_call(func, *args, **kwargs):
    """
    Wrapper para hacer llamadas seguras a la API con delay automático
    para evitar rate limiting y timeouts en tests POST
    """
    global _last_request_time
    current_time = time.time()
    
    # Asegurar al menos 0.3 segundos entre llamadas consecutivas (menos que GET)
    time_since_last = current_time - _last_request_time
    if time_since_last < 0.3:
        sleep_time = 0.3 - time_since_last
        logger.debug(f"Esperando {sleep_time:.2f}s para evitar rate limiting...")
        time.sleep(sleep_time)
    
    try:
        result = func(*args, **kwargs)
        _last_request_time = time.time()
        return result
    except Exception as e:
        logger.warning(f"Error en llamada API: {e}")
        _last_request_time = time.time()
        raise


# Admin > Customer - Group > TC_153 Crear grupo de clientes con datos válidos
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC153_crear_grupo_clientes_datos_validos(setup_customer_group_cleanup):
    """Verificar que se puede crear un grupo de clientes con datos válidos"""
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_153: Iniciando test para crear grupo de clientes con datos válidos ===")
    
    data = generate_customer_group_source_data()
    print("Generated Customer Group Data:", data)
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_post_output_schema(response.json())
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    assert response.json()["code"] == data["code"]
    assert response.json()["name"] == data["name"]


# Admin > Customer - Group > TC_154 Verificar estructura del JSON devuelto al crear
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC154_verificar_estructura_json_respuesta_creacion(setup_customer_group_cleanup):
    """Verificar que la respuesta tiene la estructura JSON correcta"""
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_154: Iniciando test para verificar estructura JSON de respuesta al crear ===")
    
    data = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_post_output_schema(response.json())
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_155 Verificar que no permita crear grupo con código duplicado
@pytest.mark.negative
@pytest.mark.regression
def test_TC155_crear_grupo_codigo_duplicado(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_155: Iniciando test para verificar código duplicado ===")
    
    data1 = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    response1 = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data1)
    
    log_request_response(endpoint, response1, headers=auth_headers, payload=data1)
    
    AssertionStatusCode.assert_status_code_201(response1)
    
    customer_group_code = response1.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data2 = generate_customer_group_source_data()
    data2["code"] = data1["code"]  # el mismo código
    response2 = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data2)
    
    log_request_response(endpoint, response2, headers=auth_headers, payload=data2)
    
    AssertionStatusCode.assert_status_code_422(response2)


# Admin > Customer - Group > TC_156 Crear grupo sin campo obligatorio 'code'
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC156_crear_grupo_sin_campo_code(auth_headers):
    logger.info("=== TC_156: Iniciando test sin campo obligatorio 'code' ===")
    
    data = generate_customer_group_source_data()
    del data["code"] #eliminar code que es obligatorio de la data que nos genera
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_157 Crear grupo sin campo obligatorio 'name'
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC157_crear_grupo_sin_campo_name(auth_headers):
    logger.info("=== TC_157: Iniciando test sin campo obligatorio 'name' ===")
    
    data = generate_customer_group_source_data()
    del data["name"]  # Eliminar campo obligatorio
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_158 Verificar que no permita crear grupo con código vacío
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC158_crear_grupo_codigo_vacio(auth_headers):
    logger.info("=== TC_158: Iniciando test con código vacío ===")
    
    data = generate_customer_group_source_data()
    data["code"] = ""
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_159 Verificar que no permita crear grupo con nombre vacío
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC159_crear_grupo_nombre_vacio(auth_headers):
    logger.info("=== TC_159: Iniciando test con nombre vacío ===")
    
    data = generate_customer_group_source_data()
    data["name"] = ""
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_160 Crear grupo con código invalido mas de 255 caracteres
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC160_crear_grupo_codigo_muy_largo(auth_headers):
    logger.info("=== TC_160: Iniciando test con código muy largo (>255 chars) ===")
    
    data = generate_customer_group_source_data()
    data["code"] = "a" * 256
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_161 Crear grupo con nombre invalido mas de 255 caracteres
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC161_crear_grupo_nombre_muy_largo(auth_headers):
    logger.info("=== TC_161: Iniciando test con nombre muy largo (>255 chars) ===")
    
    data = generate_customer_group_source_data()
    data["name"] = "a" * 256
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_162 Crear grupo con caracteres especiales no permitidos en código
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.regression
def test_TC162_crear_grupo_caracteres_especiales_codigo(auth_headers):
    logger.info("=== TC_162: Iniciando test con caracteres especiales en código ===")
    
    data = generate_customer_group_source_data()
    data["code"] = "test*code/123^!.special"
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_163 Verificar que permita crear grupo con caracteres especiales en nombre
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.regression
def test_TC163_crear_grupo_caracteres_especiales_nombre(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_163: Iniciando test para crear grupo con caracteres especiales en nombre ===")
    
    data = generate_customer_group_source_data()
    data["name"] = "Test Pablo ñáéíóú-Co_123$@$@#"
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_164 Verificar que no permita crear grupo sin token de autenticación
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
def test_TC164_crear_grupo_sin_token():
    logger.info("=== TC_164: Iniciando test sin token de autenticación ===")
    
    data = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, {}, data)
    
    log_request_response(endpoint, response, headers={}, payload=data)
    
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_165 Verificar que no permita crear grupo con token inválido
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
def test_TC165_crear_grupo_token_invalido():
    logger.info("=== TC_165: Iniciando test con token inválido ===")
    
    data = generate_customer_group_source_data()
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, invalid_headers, data)
    
    log_request_response(endpoint, response, headers=invalid_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_166 Verificar que no permita crear grupo con body JSON malformado
@pytest.mark.negative
@pytest.mark.regression
def test_TC166_crear_grupo_json_malformado(auth_headers):
    logger.info("=== TC_166: Iniciando test con JSON malformado ===")
    
    endpoint = EndpointCustomerGroup.customer_group()
    headers_with_json = {**auth_headers, 'Content-Type': 'application/json'}
    malformed_data = '{"code": "test", "name": invalid_json}'  # json inválido
    
    # Enviar JSON malformado directamente
    response = requests.post(endpoint, headers=headers_with_json, data=malformed_data)
    
    log_request_response(endpoint, response, headers=headers_with_json, payload=malformed_data)
    
    AssertionStatusCode.assert_status_code_400(response)


# Admin > Customer - Group > TC_167 Verificar que no permita crear grupo con Content-Type incorrecto
@pytest.mark.negative
@pytest.mark.regression
def test_TC167_crear_grupo_content_type_incorrecto(auth_headers):
    logger.info("=== TC_167: Iniciando test con Content-Type incorrecto ===")
    
    data = generate_customer_group_source_data()
    headers_with_text = auth_headers.copy()
    headers_with_text['Content-Type'] = 'text/plain'
    endpoint = EndpointCustomerGroup.customer_group()
    
    response = requests.post(endpoint, headers=headers_with_text, data=str(data))
    
    log_request_response(endpoint, response, headers=headers_with_text, payload=str(data))
    
    AssertionStatusCode.assert_status_code_415(response)


# Admin > Customer - Group > TC_168 Verificar que el tiempo de respuesta al crear sea menor a 3 segundos
@pytest.mark.functional
@pytest.mark.performance
@pytest.mark.regression
def test_TC168_verificar_tiempo_respuesta_creacion(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_168: Iniciando test de tiempo de respuesta para creación ===")
    
    data = generate_customer_group_source_data()
    start_time = time.time()
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    elapsed = time.time() - start_time
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    assert elapsed < 3.0, f"Tiempo de respuesta muy alto: {elapsed:.2f}s"
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_169 Verificar que permita crear múltiples grupos simultáneamente
@pytest.mark.functional
@pytest.mark.stress
@pytest.mark.regression
def test_TC169_crear_multiples_grupos_simultaneos(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_169: Iniciando test para crear múltiples grupos simultáneamente ===")
    
    responses = []
    endpoint = EndpointCustomerGroup.customer_group()
    
    for i in range(3):
        data = generate_customer_group_source_data()
        response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
        
        log_request_response(endpoint, response, headers=auth_headers, payload=data)
        
        responses.append(response)
        AssertionStatusCode.assert_status_code_201(response)
        
        customer_group_code = response.json()["code"]
        add_group_for_cleanup(customer_group_code)
        
    codes = [resp.json()["code"] for resp in responses]
    assert len(codes) == len(set(codes)), "Todos los códigos deben ser únicos"


# Admin > Customer - Group > TC_170 Verificar que permita crear grupo con código en límite superior (255 chars)
@pytest.mark.boundary
@pytest.mark.regression
def test_TC170_crear_grupo_codigo_limite_superior(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_170: Iniciando test con código en límite superior (255 chars) ===")
    
    data = generate_customer_group_source_data()
    data["code"] = "a" * 255
    endpoint = EndpointCustomerGroup.customer_group()
    
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_171 Verificar que permita crear grupo con nombre en límite superior (255 chars)
@pytest.mark.boundary
@pytest.mark.regression
def test_TC171_crear_grupo_nombre_limite_superior(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_171: Iniciando test con nombre en límite superior (255 chars) ===")
    
    data = generate_customer_group_source_data()
    data["name"] = "a" * 255
    endpoint = EndpointCustomerGroup.customer_group()
    
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_172 Verificar headers de respuesta
@pytest.mark.functional
@pytest.mark.regression
def test_TC172_verificar_headers_respuesta_creacion(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_172: Iniciando test para verificar headers de respuesta ===")
    
    data = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    headers = response.headers
    content_type = headers.get("Content-Type", "")
    assert content_type.startswith("application/ld+json"), f"Expected JSON-LD content type, got: {content_type}"


# Admin > Customer - Group > TC_173 Verificar que permita crear grupo con código de 1 carácter
@pytest.mark.boundary
@pytest.mark.regression
def test_TC173_crear_grupo_codigo_minimo(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_173: Iniciando test con código mínimo (1 char) ===")
    
    data = generate_customer_group_source_data()
    data["code"] = "a"
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_174 Verificar que permita crear grupo con nombre de 1 carácter
@pytest.mark.boundary
@pytest.mark.regression
def test_TC174_crear_grupo_nombre_minimo(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    logger.info("=== TC_174: Iniciando test con nombre mínimo (2 chars) ===")
    
    data = generate_customer_group_source_data()
    data["name"] = "Ab"  # La app pide minimo 2 caracteres
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_175 Verificar que no permita crear grupo con valores null
@pytest.mark.negative
@pytest.mark.regression
def test_TC175_crear_grupo_valores_null(auth_headers):
    logger.info("=== TC_175: Iniciando test con valores null ===")
    
    data = {
        "code": None,
        "name": None
    }
    endpoint = EndpointCustomerGroup.customer_group()
    response = safe_api_call(SyliusRequest.post, endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_400(response)