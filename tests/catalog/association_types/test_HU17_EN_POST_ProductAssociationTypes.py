import json

import pytest

from src.assertions.association_types_assertions import AssertionAssociationTypes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_product_association import EndpointAssociationTypes
from src.routes.request import SyliusRequest
from src.data.association_types import generate_association_types_source_data
from utils.logger_helpers import log_request_response


@pytest.mark.smoke
@pytest.mark.regression
def test_TC120_crear_tipo_asociacion_code_y_translations_en_US_name_validos_exitoso(teardown_association_types):
    headers, created_inventories = teardown_association_types
    payload = generate_association_types_source_data()
    url = EndpointAssociationTypes.association_types()
    AssertionAssociationTypes.assert_association_type_add_input_schema(payload)

    response = SyliusRequest.post(url, headers, payload)
    response_data = response.json()
    AssertionStatusCode.assert_status_code_201(response)
    AssertionAssociationTypes.assert_association_type_add_output_schema(response.json())

    log_request_response(url, response, headers, payload)

    AssertionAssociationTypes.assert_code_matches(response_data, payload['code'])
    AssertionAssociationTypes.assert_translation_name_matches(response_data, "en_US",
                                                              payload['translations']['en_US']['name'])
    created_inventories.append(payload['code'])

