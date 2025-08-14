import pytest

from src.assertions.association_types_assertions import AssertionAssociationTypes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_product_association import EndpointAssociationTypes
from src.routes.request import SyliusRequest
from src.data.association_types import generate_association_types_source_data
from utils.logger_helpers import log_request_response


@pytest.mark.smoke
@pytest.mark.regression
def test_TC379_eliminar_tipo_asociacion_existente_por_codigo_exitoso_204(setup_association_types):
    headers, association_type = setup_association_types
    url = EndpointAssociationTypes.code(association_type['code'])

    response = SyliusRequest.delete(url, headers)
    log_request_response(url, response, headers)

    AssertionStatusCode.assert_status_code_204(response)

    response = SyliusRequest.get(url, headers)
    log_request_response(url, response, headers)

    AssertionStatusCode.assert_status_code_404(response)
    AssertionAssociationTypes.assert_error_schema(response.json())
