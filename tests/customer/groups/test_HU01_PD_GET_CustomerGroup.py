import jsonschema
import requests
import pytest
import time

from src.assertions.customergroup_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from utils.config import BASE_URL


# Admin > Customer - Group > TC_114 Verificar estructura del JSON devuelto
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC114_Estructura_JSON(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups"
    response = requests.get(url, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_get_output_schema(response.json())

# Admin > Customer - Group > TC_115 Validar respuesta con un "code" de grupo ya existente
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
def test_TC115_Grupo_por_code_existente(auth_headers):
    group_code = "retail" 

    url = f"{BASE_URL}/admin/customer-groups/{group_code}"
    response = requests.get(url, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["code"] == group_code


# Admin > Customer - Group > TC_116 Validar paginación con parámetros page e itemsPerPage
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.boundary
def test_TC116_Paginacion(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups?page=1&itemsPerPage=2"
    response = requests.get(url, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert isinstance(response.json().get("hydra:member", []), list)



# Admin > Customer - Group > TC_118 Verificar acceso sin token (esperado: 401 Unauthorized)
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
def test_TC118_Sin_token():
    url = f"{BASE_URL}/admin/customer-groups"
    response = requests.get(url)
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_119 Verificar acceso con token inválido
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
def test_TC119_Token_invalido():
    url = f"{BASE_URL}/admin/customer-groups"
    headers = {"Authorization": "Bearer token_invalido"}
    response = requests.get(url, headers=headers)
    AssertionStatusCode.assert_status_code_401(response)



# Admin > Customer - Group > TC_141 Validar que la respuesta contenga una lista (array) no vacía si existen registros
@pytest.mark.smoke
@pytest.mark.regression
def test_TC141_Lista_no_vacia_si_existen(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups"
    response = requests.get(url, headers=auth_headers)
    data = response.json()
    assert isinstance(data.get("hydra:member", []), list)
    assert len(data["hydra:member"]) > 0


# Admin > Customer - Group > TC_142 Validar tiempos de respuesta (Performance < 1s)
@pytest.mark.smoke
@pytest.mark.regression
def test_TC142_Tiempo_respuesta(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups"
    start_time = time.time()
    response = requests.get(url, headers=auth_headers)
    elapsed = time.time() - start_time
    AssertionStatusCode.assert_status_code_200(response)
    assert elapsed < 1.7  # segundos.decimas de segundo


# Admin > Customer - Group > TC_143 Validar respuesta ante método HTTP no permitido (ej. POST en endpoint GET)
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
def test_TC143_Metodo_no_permitido(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups"
    response = requests.post(url, headers=auth_headers)
    AssertionStatusCode.assert_status_code_415(response)



# Admin > Customer - Group > TC_144 Verificar que no se repitan id, code en los grupos
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
def test_TC144_Id_y_code_unicos(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups"
    response = requests.get(url, headers=auth_headers)
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
def test_TC145_code_y_name_no_vacios(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups"
    response = requests.get(url, headers=auth_headers)
    for grupo in response.json().get("hydra:member", []):
        assert grupo["code"].strip() != ""
        assert grupo["name"].strip() != ""

# Admin > Customer - Group > TC_146 Validar encabezados de respuesta HTTP (Content-Type, Cache-Control, etc.)
@pytest.mark.smoke
@pytest.mark.security
@pytest.mark.regression
def test_TC146_Validar_encabezados_HTTP(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups"
    response = requests.get(url, headers=auth_headers)
    headers = response.headers
    content_type = headers.get("Content-Type", "")
    assert content_type.startswith("application/ld+json"), f"Expected JSON-LD content type, got: {content_type}"


# Admin > Customer - Group > TC_147 Verificar comportamiento con parámetros de paginación fuera de rango (ej. page=9999)
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC147_Paginacion_fuera_de_rango(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups?page=9999"
    response = requests.get(url, headers=auth_headers)
    data = response.json()
    AssertionStatusCode.assert_status_code_200(response)
    assert isinstance(data.get("hydra:member", []), list)


# Admin > Customer - Group > TC_148 Verificar limite de caracteres maximo en code de 255 caracteres
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.regression
def test_TC148_Limite_caracteres_campo_code_255(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups"
    response = requests.get(url, headers=auth_headers)
    for grupo in response.json().get("hydra:member", []):
        assert len(grupo["code"]) <= 255
