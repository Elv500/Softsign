import pytest

from src.assertions.attributes_assertions import AssertionAttributes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from src.data.attributes import generate_attributes_source_data


# Verificar que se pueda obterner la lista de los atributos  registrados en el submenu catálogo
# de la aplicacion Sylius.
@pytest.mark.functional
@pytest.mark.smoke
def test_TC38_Verificar_que_se_obtenga_la_lista_atributos_registrados(auth_headers):
    response = SyliusRequest.get(EndpointAttributes.attributes(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    attributes = response.json().get("hydra:member", [])
    assert isinstance(attributes, list)
    if attributes:
        assert "code" in attributes[0]
        assert "type" in attributes[0]


#Verificar que se pueda obtener un atributo cuando se realiza la busqueda por su campo code
@pytest.mark.functional
@pytest.mark.smoke
def test_TC39_Verificar_que_obtenga_un_atributo_por_code(auth_headers):
    data = generate_attributes_source_data()
    post_response = SyliusRequest.post(EndpointAttributes.attributes(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(post_response)
    code = post_response.json()["code"]

    url = EndpointAttributes.code(code)
    get_response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(get_response)
    atributo = get_response.json()
    assert atributo["code"] == code


#Verificar que se muestre un error 404 cuando se intenta realizar la busqueda de un atributo
# por un code inexistente
@pytest.mark.negative
@pytest.mark.smoke
def test_TC41_Verificar_que_no_se_permita_obtener_un_atributo_code_inexistente(auth_headers):
    url = EndpointAttributes.code("codigo_inexistente_123")
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)


# Verificar que no se muestre la lista de atributos cuando no se genero el token correctamete
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC40_Verificar_que_no_se_permita_obtener_la_lista_de_atributos_sin_token():
    url = EndpointAttributes.attributes()
    response = SyliusRequest.get(url, {})
    AssertionStatusCode.assert_status_code_401(response)


#Verificar la paginación de la lista atributos registardos en Syluis
@pytest.mark.functional
@pytest.mark.smoke
def test_TC42_Verificar_la_paginacion_de_la_lista_de_atributos(auth_headers):
    url = EndpointAttributes.attributes_with_params(page=1, itemsPerPage=2)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    atributos = response.json().get("hydra:member", [])
    assert len(atributos) <= 2


#Verificar headers de respuesta del GET de atributos
@pytest.mark.functional
@pytest.mark.smoke
def test_TC201_verificar_headers_respuesta_del_metodo_get_atributos(auth_headers):
    response = SyliusRequest.get(EndpointAttributes.attributes(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    headers = response.headers
    content_type = headers.get("Content-Type", "")
    assert content_type.startswith("application/ld+json"), f"Expected JSON-LD content type, got: {content_type}"


# Validar el schema de respuesta del metodo GET
@pytest.mark.functional
@pytest.mark.smoke
def test_TC200_Verificar_el_schema_response_del_metodo_GET(auth_headers):
        response = SyliusRequest.get(EndpointAttributes.attributes(), auth_headers)
        AssertionStatusCode.assert_status_code_200(response)
        AssertionAttributes.assert_attributes_get_output_schema(response.json())


#Verificar que no se obtenga el atributo si se realiza la busqueda con un codigo que no existe
#Verificar que se muestre un error 404
@pytest.mark.negative
@pytest.mark.smoke
def test_TC202_Verificar_que_no_se_obtenga_la_lista_atributos_con_codigo_inexistente(auth_headers):
    url = EndpointAttributes.code("codigo_inexistente_123")
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)


#Verificar que no se obtenga la lista de atributos si no se genera el tocken existosamente
#Verificar que se muestre un error 401
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC203_Verificar_que_no_se_obtenga_lista_de_atributos_sin_token():
    response = SyliusRequest.get(EndpointAttributes.attributes(),{})
    AssertionStatusCode.assert_status_code_401(response)


#Verificar que no se obtenga la lista de atributos si se genera el token invalido
#Verificar que se muestre un error 401
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC204_Verificar_que_no_se_obtenga_lista_de_atributos_con_token_invalido():
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    response = SyliusRequest.get(EndpointAttributes.attributes(), invalid_headers)
    AssertionStatusCode.assert_status_code_401(response)


