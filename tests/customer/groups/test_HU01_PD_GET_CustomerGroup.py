import jsonschema
import pytest
import time

from src.assertions.customergroup_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest

# Admin > Customer - Group > TC_114 Verificar estructura del JSON devuelto
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC114_verificar_estructura_json_devuelto(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(),auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_get_output_schema(response.json())

# Admin > Customer - Group > TC_115 Validar respuesta con un "code" de grupo ya existente
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
def test_TC115_validar_respuesta_con_code_grupo_existente(auth_headers):
    group_code = "retail" 
    response = SyliusRequest.get(EndpointCustomerGroup.code(group_code),auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["code"] == group_code
    


# Admin > Customer - Group > TC_116 Validar paginación con parámetros page e itemsPerPage
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.boundary
def test_TC116_validar_paginacion_con_parametros_page_itemsPerPage(auth_headers):
    # Usando el nuevo método con parámetros
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=2), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert isinstance(response.json().get("hydra:member", []), list)



# Admin > Customer - Group > TC_118 Verificar acceso sin token (esperado: 401 Unauthorized)
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.segurity
@pytest.mark.regression
def test_TC118_verificar_acceso_sin_token_401_unauthorized():
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), {})
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_119 Verificar acceso con token inválido
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.segurity
@pytest.mark.regression
def test_TC119_verificar_acceso_con_token_invalido():
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), invalid_headers)
    AssertionStatusCode.assert_status_code_401(response)



# Admin > Customer - Group > TC_141 Validar que la respuesta contenga una lista (array) no vacía si existen registros
@pytest.mark.smoke
@pytest.mark.regression
def test_TC141_validar_respuesta_contiene_lista_no_vacia_si_existen_registros(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    data = response.json()
    assert isinstance(data.get("hydra:member", []), list)
    assert len(data["hydra:member"]) > 0


# Admin > Customer - Group > TC_142 Validar tiempos de respuesta (Performance < 1s)
@pytest.mark.smoke
@pytest.mark.regression
def test_TC142_validar_tiempos_respuesta_performance_menor_1s(auth_headers):
    start_time = time.time()
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    elapsed = time.time() - start_time
    AssertionStatusCode.assert_status_code_200(response)
    assert elapsed < 1.7  # segundos.decimas de segundo


# Admin > Customer - Group > TC_143 Validar respuesta ante método HTTP no permitido (ej. POST en endpoint GET)
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
def test_TC143_validar_respuesta_metodo_http_no_permitido_post_en_endpoint_get(auth_headers):
    import requests
    headers_with_text = auth_headers.copy()
    headers_with_text['Content-Type'] = 'text/plain'
    response = requests.post(EndpointCustomerGroup.customer_group(), 
                           headers=headers_with_text, 
                           data="test data")
    AssertionStatusCode.assert_status_code_415(response)



# Admin > Customer - Group > TC_144 Verificar que no se repitan id, code en los grupos
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
def test_TC144_verificar_no_se_repitan_id_code_en_grupos(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    grupos = response.json().get("hydra:member", [])
    ids = [g["id"] for g in grupos]
    codes = [g["code"] for g in grupos]
    assert len(ids) == len(set(ids))
    assert len(codes) == len(set(codes))


# Admin > Customer - Group > TC_145 Verificar que los campos code y name no sean nulos o vacíos
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.usability
@pytest.mark.regression
def test_TC145_verificar_campos_code_name_no_nulos_ni_vacios(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    for grupo in response.json().get("hydra:member", []):
        assert grupo["code"].strip() != ""
        assert grupo["name"].strip() != ""

# Admin > Customer - Group > TC_146 Validar encabezados de respuesta HTTP (Content-Type, Cache-Control, etc.)
@pytest.mark.smoke
@pytest.mark.segurity
@pytest.mark.regression
def test_TC146_validar_encabezados_respuesta_http_content_type_cache_control(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    headers = response.headers
    content_type = headers.get("Content-Type", "")
    assert content_type.startswith("application/ld+json"), f"Expected JSON-LD content type, got: {content_type}"


# Admin > Customer - Group > TC_147 Verificar comportamiento con parámetros de paginación fuera de rango (ej. page=9999)
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC147_verificar_comportamiento_parametros_paginacion_fuera_rango(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group_with_params(page=9999), auth_headers)
    data = response.json()
    AssertionStatusCode.assert_status_code_200(response)
    assert isinstance(data.get("hydra:member", []), list)


# Admin > Customer - Group > TC_148 Verificar limite de caracteres maximo en code de 255 caracteres
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC148_verificar_limite_caracteres_maximo_code_255_caracteres(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    for grupo in response.json().get("hydra:member", []):
        assert len(grupo["code"]) <= 255
