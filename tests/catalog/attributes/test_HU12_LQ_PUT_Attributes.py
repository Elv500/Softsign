import pytest

from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from src.data.attributes import generate_attributes_source_data

#Verificar que NO se pueda permita realizar la actualizacion si el atributo no existe.
#Verificar que se muestre un error 404 si se intenta actualizar un atributo que no existe.

@pytest.mark.negative
@pytest.mark.regression
def test_TC47_Verificar_que_no_permitar_actualizar_un_atributo_inexistente(auth_headers):
    update_data = generate_attributes_source_data()
    url = EndpointAttributes.code("codigo_inexistente_123")
    put_response = SyliusRequest.put(url, auth_headers, update_data)
    AssertionStatusCode.assert_status_code_404(put_response)


