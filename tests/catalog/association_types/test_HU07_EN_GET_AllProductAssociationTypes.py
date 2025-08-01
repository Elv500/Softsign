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


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.association_types
def test_TC83_Obtener_tipos_de_asociacion_paginados_exitoso(auth_headers):
    url = ProductAssociationEndpoints.get_list(page="1", items_per_page="10")

    response = requests.get(url, headers=auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_response_has_items(response_data)
    AssertionAssociationTypes.assert_total_items_limit(
        response_data, expected_limit=10)
    AssertionAssociationTypes.assert_items_per_page_limit(
        response_data["hydra:member"],
        expected_limit=10
    )
    for member in response_data["hydra:member"]:
        AssertionAssociationTypes.assert_data_types(member)


@pytest.mark.regression
@pytest.mark.association_types
def test_TC84_Validar_page_limite_inferior_exitoso(auth_headers):
    url = ProductAssociationEndpoints.get_list(page="1")

    response = requests.get(url, headers=auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_response_has_items(response_data)


@pytest.mark.regression
@pytest.mark.association_types
def test_TC85_Validar_page_valor_alfabetico_error(auth_headers):
    url = ProductAssociationEndpoints.get_list(page="a")

    response = requests.get(url, headers=auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_400(response)
    AssertionAssociationTypes.assert_error_schema(response_data)
    AssertionAssociationTypes.assert_error_message(
        response_data,
        expected_message="Page should not be less than 1"
    )


@pytest.mark.regression
@pytest.mark.association_types
def test_TC86_Validar_page_caracteres_especiales_error(auth_headers):
    url = ProductAssociationEndpoints.get_list(page="@#")

    response = requests.get(url, headers=auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_400(response)
    AssertionAssociationTypes.assert_error_schema(response_data)
    AssertionAssociationTypes.assert_error_message(
        response_data,
        expected_message="Page should not be less than 1"
    )
