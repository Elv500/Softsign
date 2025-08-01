import requests
import pytest

from src.assertions.association_types_assertions import AssertionAssociationTypes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.sylius_api.product_association_endpoints import ProductAssociationEndpoints

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.association_types
def test_TC82_Obtener_todos_los_tipos_de_asociacion_de_producto_exitoso(auth_headers):

    url = ProductAssociationEndpoints.get_list()

    response = requests.get(url, headers=auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_response_has_items(response_data)
    for member in response_data["hydra:member"]:
        AssertionAssociationTypes.assert_data_types(member)
