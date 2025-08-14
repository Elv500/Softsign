import pytest

from src.assertions.association_types_assertions import AssertionAssociationTypes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_product_association import EndpointAssociationTypes
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.regression
def test_TC82_Obtener_todos_los_tipos_de_asociacion_de_producto_exitoso(auth_headers):
    url = EndpointAssociationTypes.list()
    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_response_has_items(response_data)
    for member in response_data["hydra:member"]:
        AssertionAssociationTypes.assert_data_types(member)
    log_request_response(url, response, auth_headers)


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.regression
def test_TC83_Obtener_tipos_de_asociacion_paginados_exitoso(auth_headers):
    url = EndpointAssociationTypes.list(page="1", items_per_page="10")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_response_has_items(response_data)
    AssertionAssociationTypes.assert_items_per_page_limit(
        response_data["hydra:member"],
        expected_limit=10
    )
    for member in response_data["hydra:member"]:
        AssertionAssociationTypes.assert_data_types(member)
    log_request_response(url, response, auth_headers)


@pytest.mark.boundary
@pytest.mark.functional
@pytest.mark.regression
def test_TC84_Validar_page_limite_inferior_exitoso(auth_headers):
    url = EndpointAssociationTypes.list(page="1")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_response_has_items(response_data)
    log_request_response(url, response, auth_headers)


@pytest.mark.negative
@pytest.mark.regression
def test_TC85_Validar_page_valor_alfabetico_error(auth_headers):
    url = EndpointAssociationTypes.list(page="a")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_400(response)
    AssertionAssociationTypes.assert_error_schema(response_data)
    AssertionAssociationTypes.assert_error_message(
        response_data,
        expected_message="Page should not be less than 1"
    )
    log_request_response(url, response, auth_headers)


@pytest.mark.negative
@pytest.mark.regression
def test_TC86_Validar_page_caracteres_especiales_error(auth_headers):
    url = EndpointAssociationTypes.list(page="!@#")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_400(response)
    AssertionAssociationTypes.assert_error_schema(response_data)
    AssertionAssociationTypes.assert_error_message(
        response_data,
        expected_message="Page should not be less than 1"
    )
    log_request_response(url, response, auth_headers)


@pytest.mark.negative
@pytest.mark.regression
def test_TC87_Validar_page_vacio_error(auth_headers):
    url = EndpointAssociationTypes.list(page="")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_400(response)
    AssertionAssociationTypes.assert_error_schema(response_data)
    AssertionAssociationTypes.assert_error_message(
        response_data,
        expected_message="Page should not be less than 1"
    )
    log_request_response(url, response, auth_headers)


@pytest.mark.boundary
@pytest.mark.functional
@pytest.mark.regression
def test_TC88_Validar_itemsPerPage_limite_inferior_exitoso(auth_headers):
    url = EndpointAssociationTypes.list(items_per_page="0")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_member_count(
        response_data["hydra:member"], 0)
    log_request_response(url, response, auth_headers)


@pytest.mark.negative
@pytest.mark.regression
def test_TC89_Validar_itemsPerPage_negativo_error(auth_headers):
    url = EndpointAssociationTypes.list(items_per_page=-1)
    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_400(response)
    AssertionAssociationTypes.assert_error_schema(response_data)
    AssertionAssociationTypes.assert_error_message(
        response_data,
        expected_message="Limit should not be less than 0"
    )
    log_request_response(url, response, auth_headers)


# @pytest.mark.negative
# @pytest.mark.regression
# def test_TC90_Validar_itemsPerPage_alfabetico_error(auth_headers):
#     url = EndpointAssociationTypes.list(items_per_page="a")

#     response = SyliusRequest.get(url, auth_headers)
#     response_data = response.json()

#     AssertionStatusCode.assert_status_code_400(response)
#     AssertionAssociationTypes.assert_error_schema(response_data)
#     AssertionAssociationTypes.assert_error_message(
#         response_data,
#         expected_message="Limit should not be less than 0"
#     )
#     log_request_response(url, response, auth_headers)


@pytest.mark.functional
@pytest.mark.regression
def test_TC91_Validar_orden_ascendente_code_exitoso(auth_headers):
    url = EndpointAssociationTypes.list(order="asc")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_list_ordered_by_code(
        response_data["hydra:member"], "asc")
    log_request_response(url, response, auth_headers)


@pytest.mark.functional
@pytest.mark.regression
def test_TC92_Validar_orden_descendente_code_exitoso(auth_headers):
    url = EndpointAssociationTypes.list(order="desc")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_list_ordered_by_code(
        response_data["hydra:member"], "desc")
    log_request_response(url, response, auth_headers)


@pytest.mark.functional
@pytest.mark.regression
def test_TC93_Validar_orden_invalido_exitoso(auth_headers):
    url = EndpointAssociationTypes.list(order="up")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_response_has_items(response_data)
    log_request_response(url, response, auth_headers)


@pytest.mark.functional
@pytest.mark.regression
def test_TC94_Buscar_code_valido_exitoso(auth_headers):
    url = EndpointAssociationTypes.list(code="similar_products")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_response_has_items(response_data)
    AssertionAssociationTypes.assert_code_matches_search(
        response_data["hydra:member"], "similar_products")
    log_request_response(url, response, auth_headers)


@pytest.mark.functional
@pytest.mark.regression
def test_TC95_Buscar_code_invalido_lista_vacia(auth_headers):
    url = EndpointAssociationTypes.list(code="xyzabc123")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_empty_response(response_data)
    log_request_response(url, response, auth_headers)


@pytest.mark.functional
@pytest.mark.regression
def test_TC96_Buscar_nombre_valido_exitoso(auth_headers):
    url = EndpointAssociationTypes.list(translations_name="Similar")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_response_has_items(response_data)
    AssertionAssociationTypes.assert_name_contains_search(
        response_data["hydra:member"], "Similar")
    log_request_response(url, response, auth_headers)


@pytest.mark.functional
@pytest.mark.regression
def test_TC97_Buscar_nombre_invalido_lista_vacia(auth_headers):
    url = EndpointAssociationTypes.list(translations_name="nombre_invalido")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_empty_response(response_data)
    log_request_response(url, response, auth_headers)


@pytest.mark.security
@pytest.mark.negative
@pytest.mark.regression
def test_TC98_Validar_autenticacion_invalida_error_401():
    invalid_token = "invalid.token.123"
    invalid_headers = {"Authorization": f"Bearer {invalid_token}"}
    url = EndpointAssociationTypes.list()

    response = SyliusRequest.get(url, invalid_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_401(response)
    AssertionAssociationTypes.assert_invalid_jwt_error(response_data)
    log_request_response(url, response, invalid_headers)


@pytest.mark.functional
@pytest.mark.regression
def test_TC99_Verificar_combinacion_parametros_exitoso(auth_headers):
    url = EndpointAssociationTypes.list(
        page=1, items_per_page=20, order="desc")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_200(response)
    AssertionAssociationTypes.assert_association_types_list_schema(
        response_data)
    AssertionAssociationTypes.assert_response_has_items(response_data)
    AssertionAssociationTypes.assert_items_per_page_limit(
        response_data["hydra:member"], 20)
    AssertionAssociationTypes.assert_list_ordered_by_code(
        response_data["hydra:member"], "desc")
    log_request_response(url, response, auth_headers)


@pytest.mark.negative
@pytest.mark.regression
def test_TC101_Validar_page_negativo_orden_valido_error(auth_headers):
    url = EndpointAssociationTypes.list(page=-1, order="asc")

    response = SyliusRequest.get(url, auth_headers)
    response_data = response.json()

    AssertionStatusCode.assert_status_code_400(response)
    AssertionAssociationTypes.assert_error_schema(response_data)
    AssertionAssociationTypes.assert_error_message(
        response_data,
        expected_message="Page should not be less than 1"
    )
    log_request_response(url, response, auth_headers)
