import jsonschema
import pytest
import time
from faker import Faker

from src.assertions.customergroup_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from src.data.customer_group import generate_customer_group_source_data


# Admin > Customer - Group > TC_153 Crear grupo de clientes con datos válidos
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC153_crear_grupo_clientes_datos_validos(auth_headers):
    """Verificar que se puede crear un grupo de clientes con datos válidos"""
    data = generate_customer_group_source_data()
    print("Generated Customer Group Data:", data)
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_post_output_schema(response.json())
    
    assert response.json()["code"] == data["code"]
    assert response.json()["name"] == data["name"]


# Admin > Customer - Group > TC_154 Verificar estructura del JSON devuelto al crear
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC154_verificar_estructura_json_respuesta_creacion(auth_headers):
    """Verificar que la respuesta tiene la estructura JSON correcta"""
    data = generate_customer_group_source_data()
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_post_output_schema(response.json())


# Admin > Customer - Group > TC_155 Verificar que no permita crear grupo con código duplicado
@pytest.mark.negative
@pytest.mark.regression
def test_TC155_crear_grupo_codigo_duplicado(auth_headers):
    data1 = generate_customer_group_source_data()
    response1 = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data1)
    AssertionStatusCode.assert_status_code_201(response1)
    
    data2 = generate_customer_group_source_data()
    data2["code"] = data1["code"]  # Usar el mismo código
    response2 = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data2)
    AssertionStatusCode.assert_status_code_422(response2)


# Admin > Customer - Group > TC_156 Crear grupo sin campo obligatorio 'code'
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC156_crear_grupo_sin_campo_code(auth_headers):
    data = generate_customer_group_source_data()
    del data["code"]  # Eliminar campo obligatorio
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_157 Crear grupo sin campo obligatorio 'name'
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC157_crear_grupo_sin_campo_name(auth_headers):
    data = generate_customer_group_source_data()
    del data["name"]  # Eliminar campo obligatorio
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_158 Verificar que no pemrita crear grupo con código vacío
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC158_crear_grupo_codigo_vacio(auth_headers):
    data = generate_customer_group_source_data()
    data["code"] = ""
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_159 Verificar que no pemrita crear grupo con nombre vacío
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC159_crear_grupo_nombre_vacio(auth_headers):
    data = generate_customer_group_source_data()
    data["name"] = ""
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_160 Crear grupo con código invalido mas de 255 caracteres
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC160_crear_grupo_codigo_muy_largo(auth_headers):
    data = generate_customer_group_source_data()
    data["code"] = "a" * 256
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_161 Crear grupo con nombre invalido mas de 255 caracteres
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC161_crear_grupo_nombre_muy_largo(auth_headers):
    data = generate_customer_group_source_data()
    data["name"] = "a" * 256
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_162 Crear grupo con caracteres especiales no permitidos en código
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.regression
def test_TC162_crear_grupo_caracteres_especiales_codigo(auth_headers):
    data = generate_customer_group_source_data()
    data["code"] = "test*code/123^!.special"
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_163 Verificar que permita crear grupo con caracteres especiales en nombre
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.regression
def test_TC163_crear_grupo_caracteres_especiales_nombre(auth_headers):
    data = generate_customer_group_source_data()
    data["name"] = "Test Pablo ñáéíóú-Co_123$@$@#"
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(response)


# Admin > Customer - Group > TC_164 Verificar que no permita crear grupo sin token de autenticación
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
def test_TC164_crear_grupo_sin_token():
    data = generate_customer_group_source_data()
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), {}, data)
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_165 Verificar que no permita crear grupo con token inválido
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
def test_TC165_crear_grupo_token_invalido():
    data = generate_customer_group_source_data()
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), invalid_headers, data)
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_166 Verificar que no permita crear grupo con body JSON malformado
@pytest.mark.negative
@pytest.mark.regression
def test_TC166_crear_grupo_json_malformado(auth_headers):
    import requests
    # Enviar JSON malformado directamente
    response = requests.post(
        EndpointCustomerGroup.customer_group(),
        headers={**auth_headers, 'Content-Type': 'application/json'},
        data='{"code": "test", "name": invalid_json}'  # json inválido
    )
    AssertionStatusCode.assert_status_code_400(response)


# Admin > Customer - Group > TC_167 Verificar que no permita crear grupo con Content-Type incorrecto
@pytest.mark.negative
@pytest.mark.regression
def test_TC167_crear_grupo_content_type_incorrecto(auth_headers):
    import requests
    data = generate_customer_group_source_data()
    headers_with_text = auth_headers.copy()
    headers_with_text['Content-Type'] = 'text/plain'
    
    response = requests.post(
        EndpointCustomerGroup.customer_group(),
        headers=headers_with_text,
        data=str(data)
    )
    AssertionStatusCode.assert_status_code_415(response)


# Admin > Customer - Group > TC_168 Verificar que el tiemps de respuesta al crear sea menor a 3 segundos
@pytest.mark.functional
@pytest.mark.performance
@pytest.mark.regression
def test_TC168_verificar_tiempo_respuesta_creacion(auth_headers):
    data = generate_customer_group_source_data()
    start_time = time.time()
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    elapsed = time.time() - start_time
    
    AssertionStatusCode.assert_status_code_201(response)
    assert elapsed < 3.0


# Admin > Customer - Group > TC_169 Verificar que permita crear múltiples grupos simultáneamente
@pytest.mark.functional
@pytest.mark.stress
@pytest.mark.regression
def test_TC169_crear_multiples_grupos_simultaneos(auth_headers):
    responses = []
    for i in range(3):
        data = generate_customer_group_source_data()
        response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
        responses.append(response)
        AssertionStatusCode.assert_status_code_201(response)
    codes = [resp.json()["code"] for resp in responses]
    assert len(codes) == len(set(codes))


# Admin > Customer - Group > TC_170 Verificar que permita crear grupo con código en límite superior (255 chars)
@pytest.mark.boundary
@pytest.mark.regression
def test_TC170_crear_grupo_codigo_limite_superior(auth_headers):
    data = generate_customer_group_source_data()
    data["code"] = "a" * 255
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(response)


# Admin > Customer - Group > TC_171 Verificar que permita crear grupo con nombre en límite superior (255 chars)
@pytest.mark.boundary
@pytest.mark.regression
def test_TC171_crear_grupo_nombre_limite_superior(auth_headers):
    data = generate_customer_group_source_data()
    data["name"] = "a" * 255
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(response)


# Admin > Customer - Group > TC_172 Verificar headers de respuesta
@pytest.mark.functional
@pytest.mark.regression
def test_TC172_verificar_headers_respuesta_creacion(auth_headers):
    data = generate_customer_group_source_data()
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(response)
    
    headers = response.headers
    content_type = headers.get("Content-Type", "")
    assert content_type.startswith("application/ld+json"), f"Expected JSON-LD content type, got: {content_type}"


# Admin > Customer - Group > TC_173 Verificar que permita crear grupo con código de 1 carácter
@pytest.mark.boundary
@pytest.mark.regression
def test_TC173_crear_grupo_codigo_minimo(auth_headers):
    data = generate_customer_group_source_data()
    data["code"] = "a"
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(response)


# Admin > Customer - Group > TC_174 Verificar que permita crear grupo con nombre de 1 carácter
@pytest.mark.boundary
@pytest.mark.regression
def test_TC174_crear_grupo_nombre_minimo(auth_headers):
    data = generate_customer_group_source_data()
    data["name"] = "Ab"  #La app pide minimo 2 caracteres
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(response)



# Admin > Customer - Group > TC_175 Verificar que no permita crear grupo con valores null
@pytest.mark.negative
@pytest.mark.regression
def test_TC175_crear_grupo_valores_null(auth_headers):
    data = {
        "code": None,
        "name": None
    }
    response = SyliusRequest.post(EndpointCustomerGroup.customer_group(), auth_headers, data)
    AssertionStatusCode.assert_status_code_400(response)