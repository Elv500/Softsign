import pytest
import time

from src.assertions.customergroup_assertions.customer_group_errors_assertions import AssertionCustomerGroupErrors
from src.assertions.customergroup_assertions.customer_group_post_content_assertions import AssertionCustomerGroupCreate
from src.assertions.customergroup_assertions.customer_group_schema_assertions import AssertionCustomerGroup
from src.assertions.customergroup_assertions.customer_group_performance_assertions import AssertionCustomerGroupPerformance
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from src.data.customer_group import generate_customer_group_source_data
from utils.logger_helpers import log_request_response

# Admin > Customer - Group > TC_153 Crear grupo de clientes con datos válidos
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC153_crear_grupo_clientes_datos_validos(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup

    data = generate_customer_group_source_data()

    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)

    log_request_response(endpoint, response, headers=auth_headers, payload=data)

    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_output_schema(response.json())

    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)

    assert response.json()["code"] == data["code"]
    assert response.json()["name"] == data["name"]

# Admin > Customer - Group > TC_154 Verificar estructura del JSON devuelto al crear
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC154_verificar_estructura_json_respuesta_creacion(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    data = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_output_schema(response.json())
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_155 Verificar que no permita crear grupo con código duplicado
@pytest.mark.negative
@pytest.mark.high
def test_TC155_crear_grupo_codigo_duplicado(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    data1 = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    response1 = SyliusRequest.post(endpoint, auth_headers, data1)
    
    log_request_response(endpoint, response1, headers=auth_headers, payload=data1)
    
    AssertionStatusCode.assert_status_code_201(response1)
    
    customer_group_code = response1.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data2 = generate_customer_group_source_data()
    data2["code"] = data1["code"]
    response2 = SyliusRequest.post(endpoint, auth_headers, data2)
    
    log_request_response(endpoint, response2, headers=auth_headers, payload=data2)
    
    AssertionStatusCode.assert_status_code_422(response2)
    AssertionCustomerGroupErrors.assert_validation_error(response2)


# Admin > Customer - Group > TC_156 Crear grupo sin campo obligatorio 'code'
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.high
def test_TC156_crear_grupo_sin_campo_code(auth_headers):
    
    data = generate_customer_group_source_data()
    del data["code"]
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_validation_error(response)


# Admin > Customer - Group > TC_157 Crear grupo sin campo obligatorio 'name'
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.high
def test_TC157_crear_grupo_sin_campo_name(auth_headers):
    
    data = generate_customer_group_source_data()
    del data["name"]
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_validation_error(response)


# Admin > Customer - Group > TC_158 Verificar que no permita crear grupo con código vacío
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.medium
def test_TC158_crear_grupo_codigo_vacio(auth_headers):
    
    data = generate_customer_group_source_data()
    data["code"] = ""
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_validation_error(response)


# Admin > Customer - Group > TC_159 Verificar que no permita crear grupo con nombre vacío
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.medium
def test_TC159_crear_grupo_nombre_vacio(auth_headers):
    
    data = generate_customer_group_source_data()
    data["name"] = ""
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_validation_error(response)


# Admin > Customer - Group > TC_160 Crear grupo con código invalido mas de 255 caracteres
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.medium
def test_TC160_crear_grupo_codigo_muy_largo(auth_headers):
    
    data = generate_customer_group_source_data()
    data["code"] = "a" * 256
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_validation_error(response)


# Admin > Customer - Group > TC_161 Crear grupo con nombre invalido mas de 255 caracteres
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.medium
def test_TC161_crear_grupo_nombre_muy_largo(auth_headers):
    
    data = generate_customer_group_source_data()
    data["name"] = "a" * 256
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_validation_error(response)


# Admin > Customer - Group > TC_162 Crear grupo con caracteres especiales no permitidos en código
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.medium
def test_TC162_crear_grupo_caracteres_especiales_codigo(auth_headers):
    
    data = generate_customer_group_source_data()
    data["code"] = "test*code/123^!.special"
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_validation_error(response)


# Admin > Customer - Group > TC_163 Verificar que permita crear grupo con caracteres especiales en nombre
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.medium
def test_TC163_crear_grupo_caracteres_especiales_nombre(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    data = generate_customer_group_source_data()
    data["name"] = "Test Pablo ñáéíóú-Co_123$@$@#"
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_output_schema(response.json())
    AssertionCustomerGroupCreate.assert_customer_group_response(data, response.json())
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_164 Verificar que no permita crear grupo sin token de autenticación
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.high
def test_TC164_crear_grupo_sin_token():
    
    data = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, {}, data)
    
    log_request_response(endpoint, response, headers={}, payload=data)
    
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_165 Verificar que no permita crear grupo con token inválido
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.high
def test_TC165_crear_grupo_token_invalido():
    
    data = generate_customer_group_source_data()
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, invalid_headers, data)
    
    log_request_response(endpoint, response, headers=invalid_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_166 Verificar que no permita crear grupo con body JSON malformado
@pytest.mark.negative
@pytest.mark.medium
def test_TC166_crear_grupo_json_malformado(auth_headers):
    
    endpoint = EndpointCustomerGroup.customer_group()
    headers_with_json = {**auth_headers, 'Content-Type': 'application/json'}
    # Enviar JSON malformado usando raw data
    import requests
    response = requests.post(
        endpoint,
        headers=headers_with_json,
        data='{"code": "test", "name": invalid_json}'
    )
    
    log_request_response(endpoint, response, headers=headers_with_json)
    
    AssertionStatusCode.assert_status_code_400(response)


# Admin > Customer - Group > TC_167 Verificar que no permita crear grupo con Content-Type incorrecto
@pytest.mark.negative
@pytest.mark.medium
def test_TC167_crear_grupo_content_type_incorrecto(auth_headers):
    
    data = generate_customer_group_source_data()
    headers_with_text = auth_headers.copy()
    headers_with_text['Content-Type'] = 'text/plain'
    endpoint = EndpointCustomerGroup.customer_group()
    
    # Para content-type incorrecto, necesitamos usar requests directamente
    import requests
    response = requests.post(
        endpoint,
        headers=headers_with_text,
        data=str(data)
    )
    
    log_request_response(endpoint, response, headers=headers_with_text)
    
    AssertionStatusCode.assert_status_code_415(response)


# Admin > Customer - Group > TC_168 Verificar que el tiempo de respuesta al crear sea menor a 3 segundos
@pytest.mark.functional
@pytest.mark.performance
@pytest.mark.medium
def test_TC168_verificar_tiempo_respuesta_creacion(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    data = generate_customer_group_source_data()
    start_time = time.time()
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    elapsed = time.time() - start_time
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_output_schema(response.json())
    AssertionCustomerGroupPerformance.assert_creation_response_time(elapsed)
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_169 Verificar que permita crear múltiples grupos simultáneamente
@pytest.mark.functional
@pytest.mark.stress
@pytest.mark.low
def test_TC169_crear_multiples_grupos_simultaneos(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    responses = []
    endpoint = EndpointCustomerGroup.customer_group()
    
    for i in range(3):
        data = generate_customer_group_source_data()
        response = SyliusRequest.post(endpoint, auth_headers, data)
        
        log_request_response(endpoint, response, headers=auth_headers, payload=data)
        
        responses.append(response)
        AssertionStatusCode.assert_status_code_201(response)
        AssertionCustomerGroup.assert_customer_group_output_schema(response.json())
        
        customer_group_code = response.json()["code"]
        add_group_for_cleanup(customer_group_code)
        
    AssertionCustomerGroupPerformance.assert_multiple_creation_uniqueness(responses)


# Admin > Customer - Group > TC_170 Verificar que permita crear grupo con código en límite superior (255 chars)
@pytest.mark.boundary
@pytest.mark.low
def test_TC170_crear_grupo_codigo_limite_superior(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    data = generate_customer_group_source_data()
    data["code"] = "a" * 255
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_output_schema(response.json())
    AssertionCustomerGroupCreate.assert_customer_group_response(data, response.json())
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_171 Verificar que permita crear grupo con nombre en límite superior (255 chars)
@pytest.mark.boundary
@pytest.mark.low
def test_TC171_crear_grupo_nombre_limite_superior(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    data = generate_customer_group_source_data()
    data["name"] = "a" * 255
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_output_schema(response.json())
    AssertionCustomerGroupCreate.assert_customer_group_response(data, response.json())
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_172 Verificar headers de respuesta
@pytest.mark.functional
@pytest.mark.low
def test_TC172_verificar_headers_respuesta_creacion(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    data = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_output_schema(response.json())
    AssertionCustomerGroupPerformance.assert_creation_content_type_header(response.headers)
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_173 Verificar que permita crear grupo con código de 1 carácter
@pytest.mark.boundary
@pytest.mark.medium
def test_TC173_crear_grupo_codigo_minimo(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    data = generate_customer_group_source_data()
    data["code"] = "a"
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_output_schema(response.json())
    AssertionCustomerGroupCreate.assert_customer_group_response(data, response.json())
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)


# Admin > Customer - Group > TC_430 Verificar que permita crear grupo con nombre de 2 carácter
@pytest.mark.boundary
@pytest.mark.low
def test_TC430_crear_grupo_nombre_minimo(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    data = generate_customer_group_source_data()
    data["name"] = "Ab"  #La app pide minimo 2 caracteres
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_output_schema(response.json())
    AssertionCustomerGroupCreate.assert_customer_group_response(data, response.json())
    
    customer_group_code = response.json()["code"]
    add_group_for_cleanup(customer_group_code)



# Admin > Customer - Group > TC_270 Verificar que no permita crear grupo con valores null
@pytest.mark.negative
@pytest.mark.medium
def test_TC270_crear_grupo_valores_null(auth_headers):

    data = {
        "code": None,
        "name": None
    }
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_400(response)