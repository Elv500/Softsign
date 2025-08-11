import pytest

from src.assertions.attributes_assertions import AssertionAttributes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from src.data.attributes import generate_attributes_source_data
from utils.logger_helpers import log_request_response


@pytest.mark.smoke
@pytest.mark.functional
#Verificar que se permita crear un nuevo atributo en catalagos de la aplicacion Sylius.
#Verificar que se muestre un status code 201
def test_TC51_Verificar_que_se_permita_crear_nuevo_attribute_en_catalagos(setup_add_attributes):
    headers, created_attributes = setup_add_attributes
    payload = generate_attributes_source_data()
    response = SyliusRequest.post(EndpointAttributes.attributes(), headers, payload)
    log_request_response(EndpointAttributes.attributes(), response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionAttributes.assert_attributes_post_output_schema(response.json())
    created_attributes.append(response.json())


@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.positive
#Verificar que se permita crear un nuevo atributo con campos requeridos.
#Verificar que se muestre un status code 201
def test_TC52_Verificar_que_se_permita_crear_un_atributo_con_campos_requeridos(setup_add_attributes):
    headers, created_attributes = setup_add_attributes
    payload = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionAttributes.assert_attributes_post_input_schema(payload)
    AssertionAttributes.assert_attributes_post_output_schema(response.json())
    assert response.json()["code"] == payload["code"]
    assert response.json()["translations"]["en_US"]["name"] == payload["translations"]["en_US"]["name"]

