import pytest

from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from src.data.attributes import generate_attributes_source_data
from utils.logger_helpers import log_request_response

@pytest.mark.e2e
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
# Admin> Catalog> Attributes> TC_416: Este test E2E  valida los metodos POST-GET-DELETE-GET de un atributo.
def test_TC416_e2e_attributes(auth_headers):
    # Crear nuevo atributo (POST)
    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    response_post = SyliusRequest.post(url, auth_headers, data)
    log_request_response(url, response_post, headers=auth_headers, payload=data)
    AssertionStatusCode.assert_status_code_201(response_post)

    created_attribute = response_post.json()
    attribute_code = created_attribute["code"]

    # Obtener el nuevo atributo creado (GET)
    get_endpoint = EndpointAttributes.code(attribute_code)
    get_response = SyliusRequest.get(get_endpoint, auth_headers)
    log_request_response(get_endpoint, get_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(get_response)

    retrieved_attribute = get_response.json()
    assert retrieved_attribute["code"] == attribute_code
    assert retrieved_attribute["translations"]["en_US"]["name"] == data["translations"]["en_US"]["name"]

    #Eliminar el atributo creado (DELETE)
    delete_endpoint = EndpointAttributes.code(attribute_code)
    delete_response = SyliusRequest.delete(delete_endpoint, auth_headers)
    log_request_response(delete_endpoint, delete_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)

    #Verificar que el atributo eliminado no existe (GET)
    get_after_delete_response = SyliusRequest.get(get_endpoint, auth_headers)
    log_request_response(get_endpoint, get_after_delete_response, headers=auth_headers)
    assert get_after_delete_response.status_code == 404