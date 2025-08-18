import pytest

from src.routes.request import SyliusRequest
from src.assertions.status_code_assertions import AssertionStatusCode
from src.data.taxCategory import generate_tax_category_data
from src.routes.endpoint_tax_category import EndpointTaxCategory
from utils.logger_helpers import log_request_response

@pytest.mark.e2e
@pytest.mark.tax_category
def test_full_tax_category_crud_flow(setup_e2e_tax_category):
    auth_headers, created_tax_categories = setup_e2e_tax_category

    # 1. Crear
    initial_data = generate_tax_category_data()
    create_url = EndpointTaxCategory.tax_category()
    create_response = SyliusRequest.post(create_url, auth_headers, initial_data)
    log_request_response(create_url, create_response, headers=auth_headers, payload=initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    created_category = create_response.json()
    category_code = created_category.get("code")
    created_tax_categories.append({"code": category_code})

    # 2. Listar (usando filtro por code para evitar paginación)
    list_url = f"{EndpointTaxCategory.tax_category()}?code={category_code}"
    list_response = SyliusRequest.get(list_url, auth_headers)
    log_request_response(list_url, list_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(list_response)

    # 3. Editar
    update_data = {
        "name": "IVA Actualizado",
        "description": "Descripción modificada"
    }
    update_url = EndpointTaxCategory.code(category_code)
    update_response = SyliusRequest.put(update_url, auth_headers, update_data)
    log_request_response(update_url, update_response, headers=auth_headers, payload=update_data)
    AssertionStatusCode.assert_status_code_200(update_response)

    # 4. Eliminar
    delete_url = EndpointTaxCategory.code(category_code)
    delete_response = SyliusRequest.delete(delete_url, auth_headers)
    log_request_response(delete_url, delete_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)

    # 5. Verificar no existencia
    get_deleted_response = SyliusRequest.get(delete_url, auth_headers)
    log_request_response(delete_url, get_deleted_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_404(get_deleted_response)