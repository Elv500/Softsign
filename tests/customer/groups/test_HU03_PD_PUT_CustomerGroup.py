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

# Admin > Customer - Group > TC_271 Actualizar grupo de clientes con datos válidos
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC271_actualizar_grupo_clientes_datos_validos(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    update_data = {
        "name": "Updated Customer Group Name"
    }
    
    AssertionCustomerGroup.assert_customer_group_edit_input_schema(update_data)
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, update_data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=update_data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())
    
    AssertionCustomerGroupCreate.assert_customer_group_response(
        {"name": "Updated Customer Group Name", "code": customer_group_code}, 
        response.json()
    )


# Admin > Customer - Group > TC_272 Verificar estructura del JSON devuelto al actualizar
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC272_verificar_estructura_json_respuesta_actualizacion(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    update_data = {
        "name": "Updated Customer Group Name"
    }
    
    AssertionCustomerGroup.assert_customer_group_edit_input_schema(update_data)
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, update_data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=update_data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())


# Admin > Customer - Group > TC_273 Verificar que no permita actualizar grupo con código inexistente
@pytest.mark.negative
@pytest.mark.high
def test_TC273_actualizar_grupo_codigo_inexistente(auth_headers):
    
    codigo_inexistente = "grupo_inexistente_12345"
    data = generate_customer_group_source_data()
    data["code"] = codigo_inexistente
    endpoint = EndpointCustomerGroup.code(codigo_inexistente)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_404(response)


# Admin > Customer - Group > TC_274 Actualizar grupo sin campo obligatorio 'name'
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.xfail(reason="Known issue BugId: CG-03 Permite actualizar el campo name vacio cuando es obligatorio", run=True)
@pytest.mark.high
def test_TC274_actualizar_grupo_sin_campo_name(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {}  
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_275 Verificar que el campo code en el body es ignorado
@pytest.mark.functional
@pytest.mark.medium
def test_TC275_actualizar_grupo_campo_code_ignorado(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    original_code = create_response.json()["code"]
    add_group_for_cleanup(original_code)
    
    data = {
        "code": "codigo_diferente_que_sera_ignorado",
        "name": "Nombre Actualizado - Code Ignorado"
    }
    endpoint = EndpointCustomerGroup.code(original_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())
    
    AssertionCustomerGroupCreate.assert_customer_group_response(
        {"name": "Nombre Actualizado - Code Ignorado", "code": original_code}, 
        response.json()
    )


# Admin > Customer - Group > TC_276 Verificar que code vacío en body es ignorado
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.medium
def test_TC276_actualizar_grupo_code_vacio_ignorado(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    original_code = create_response.json()["code"]
    add_group_for_cleanup(original_code)
    
    data = {
        "code": "",
        "name": "Nombre Actualizado - Code Vacío"
    }
    endpoint = EndpointCustomerGroup.code(original_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())
    
    AssertionCustomerGroupCreate.assert_customer_group_response(
        {"name": "Nombre Actualizado - Code Vacío", "code": original_code}, 
        response.json()
    )


# Admin > Customer - Group > TC_277 Verificar que code con caracteres especiales en body es ignorado
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.medium
def test_TC277_actualizar_grupo_code_caracteres_especiales_ignorado(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    original_code = create_response.json()["code"]
    add_group_for_cleanup(original_code)
    
    data = {
        "code": "test*code/123^!.special@#$%",
        "name": "Nombre Actualizado - Code Especial"
    }
    endpoint = EndpointCustomerGroup.code(original_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())
    
    AssertionCustomerGroupCreate.assert_customer_group_response(
        {"name": "Nombre Actualizado - Code Especial", "code": original_code}, 
        response.json()
    )


# Admin > Customer - Group > TC_278 Verificar que code muy largo en body es ignorado
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.medium
def test_TC278_actualizar_grupo_code_muy_largo_ignorado(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    original_code = create_response.json()["code"]
    add_group_for_cleanup(original_code)
    
    data = {
        "code": "a" * 260, 
        "name": "Nombre Actualizado - Code Largo"
    }
    endpoint = EndpointCustomerGroup.code(original_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())
    
    AssertionCustomerGroupCreate.assert_customer_group_response(
        {"name": "Nombre Actualizado - Code Largo", "code": original_code}, 
        response.json()
    )


# Admin > Customer - Group > TC_280 Verificar que code null en body es ignorado
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.medium
def test_TC280_actualizar_grupo_code_null_ignorado(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    original_code = create_response.json()["code"]
    add_group_for_cleanup(original_code)
    
    data = {
        "code": None,
        "name": "Nombre Actualizado - Code Null"
    }
    endpoint = EndpointCustomerGroup.code(original_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())
    
    AssertionCustomerGroupCreate.assert_customer_group_response(
        {"name": "Nombre Actualizado - Code Null", "code": original_code}, 
        response.json()
    )


# Admin > Customer - Group > TC_281 Verificar que no permita actualizar grupo con nombre vacío
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.high
def test_TC281_actualizar_grupo_nombre_vacio(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": ""
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_282 Verificar que no permita nombre muy largo
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.high
def test_TC282_actualizar_grupo_nombre_muy_largo(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "a" * 256
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_283 Verificar que permita actualizar grupo con caracteres especiales en nombre
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.medium
def test_TC283_actualizar_grupo_nombre_caracteres_especiales(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "Test Pablo ñáéíóú-Co_123$@$@#"
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())


# Admin > Customer - Group > TC_284 Verificar que no permita actualizar grupo sin token de autenticación
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.high
def test_TC284_actualizar_grupo_sin_token():
    
    codigo_existente = "retail"
    data = {
        "name": "Nombre Actualizado Sin Token"
    }
    endpoint = EndpointCustomerGroup.code(codigo_existente)
    response = SyliusRequest.put(endpoint, {}, data)
    
    log_request_response(endpoint, response, headers={}, payload=data)
    
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_285 Verificar que no permita actualizar grupo con token inválido
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.high
def test_TC285_actualizar_grupo_token_invalido():
    
    codigo_existente = "retail"
    data = {
        "name": "Nombre Actualizado Token Inválido"
    }
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    endpoint = EndpointCustomerGroup.code(codigo_existente)
    response = SyliusRequest.put(endpoint, invalid_headers, data)
    
    log_request_response(endpoint, response, headers=invalid_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_286 Verificar que no permita actualizar grupo con body JSON malformado
@pytest.mark.negative
@pytest.mark.medium
def test_TC286_actualizar_grupo_json_malformado(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    headers_with_json = {**auth_headers, 'Content-Type': 'application/json'}
    # Para JSON malformado necesitamos usar requests directamente
    import requests
    response = requests.put(
        endpoint,
        headers=headers_with_json,
        data='{"name": invalid_json}'
    )
    
    log_request_response(endpoint, response, headers=headers_with_json)
    
    AssertionStatusCode.assert_status_code_400(response)


# Admin > Customer - Group > TC_287 Verificar que no permita actualizar grupo con Content-Type incorrecto
@pytest.mark.negative
@pytest.mark.medium
def test_TC287_actualizar_grupo_content_type_incorrecto(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "Nombre Actualizado"
    }
    headers_with_text = auth_headers.copy()
    headers_with_text['Content-Type'] = 'text/plain'
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    
    # Para content-type incorrecto necesitamos usar requests directamente
    import requests
    response = requests.put(
        endpoint,
        headers=headers_with_text,
        data=str(data)
    )
    
    log_request_response(endpoint, response, headers=headers_with_text)
    
    AssertionStatusCode.assert_status_code_415(response)


# Admin > Customer - Group > TC_288 Verificar que el tiempo de respuesta al actualizar sea menor a 3 segundos
@pytest.mark.functional
@pytest.mark.performance
@pytest.mark.medium
def test_TC288_verificar_tiempo_respuesta_actualizacion(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "Nombre Actualizado Performance"
    }
    start_time = time.time()
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    elapsed = time.time() - start_time
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())
    
    performance_assertions = AssertionCustomerGroupPerformance()
    performance_assertions.assert_update_response_time(elapsed)


# Admin > Customer - Group > TC_289 Verificar que permita actualizar grupo con nombre en límite superior (255 chars)
@pytest.mark.boundary
@pytest.mark.medium
def test_TC289_actualizar_grupo_nombre_limite_superior(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "a" * 255
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())


# Admin > Customer - Group > TC_290 Verificar headers de respuesta
@pytest.mark.functional
@pytest.mark.low
def test_TC290_verificar_headers_respuesta_actualizacion(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "Nombre Actualizado Headers"
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())
    
    performance_assertions = AssertionCustomerGroupPerformance()
    performance_assertions.assert_update_content_type_header(response)


# Admin > Customer - Group > TC_291 Verificar que permita actualizar grupo con nombre mínimo
@pytest.mark.boundary
@pytest.mark.low
def test_TC291_actualizar_grupo_nombre_minimo(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "Ab"
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())


# Admin > Customer - Group > TC_292 Verificar que no permita actualizar grupo con valores null
@pytest.mark.negative
@pytest.mark.medium
def test_TC292_actualizar_grupo_valores_null(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "code": None,
        "name": None
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_400(response)
