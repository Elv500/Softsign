import pytest

from src.routes.endpoint_tax_category import EndpointTaxCategory
from src.resources.call_request.taxCategory_call import TaxCategoryCall
from src.resources.payloads.payload_taxCategory import PayloadTaxCategory
from src.data.taxCategory import generate_tax_category_data
from src.routes.request import SyliusRequest


@pytest.fixture(scope="module")
def setup_teardown_view_tax_category(auth_headers):
    payload_tax1 = PayloadTaxCategory.build_payload_tax_category(generate_tax_category_data())
    payload_tax2 = PayloadTaxCategory.build_payload_tax_category(generate_tax_category_data())

    response1 = TaxCategoryCall.create(auth_headers, payload_tax1)
    response2 = TaxCategoryCall.create(auth_headers, payload_tax2)
    tax_category1_data = response1.json()
    tax_category2_data = response2.json()

    yield auth_headers, tax_category1_data, tax_category2_data

    TaxCategoryCall().delete(auth_headers, tax_category1_data['code'])
    TaxCategoryCall().delete(auth_headers, tax_category2_data['code'])

@pytest.fixture(scope="function")
def setup_add_tax_category(auth_headers):
    created_tax_categories = []
    yield auth_headers, created_tax_categories

    for category in created_tax_categories:
        try:

            if isinstance(category, dict) and "code" in category:
                code = category["code"]

            elif isinstance(category, str):
                code = category

            elif hasattr(category, "json") and isinstance(category.json(), dict) and "code" in category.json():
                code = category.json()["code"]
            else:
                print(f"[Cleanup] Formato desconocido: {category}")
                continue
            url = EndpointTaxCategory.code(code)
            response = SyliusRequest.delete(url, auth_headers)
            if response.status_code != 204:
                print(f"[Cleanup] Error al eliminar tax category {code}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[Cleanup] Excepción al eliminar categoría: {category}. Error: {e}")

@pytest.fixture(scope="class")
def setup_edit_tax_category(auth_headers):
    payload_tax = PayloadTaxCategory.build_payload_tax_category(generate_tax_category_data())
    response = TaxCategoryCall.create(auth_headers, payload_tax)
    tax_category_data = response.json()
    # Verifica que tiene 'code'
    assert "code" in tax_category_data, f"La respuesta de creación no contiene 'code': {tax_category_data}"
    yield auth_headers, tax_category_data
    TaxCategoryCall().delete(auth_headers, tax_category_data["code"])

@pytest.fixture(scope="function")
def setup_create_tax_category(auth_headers):
    payload_tax = PayloadTaxCategory.build_payload_tax_category(generate_tax_category_data())
    response = TaxCategoryCall.create(auth_headers, payload_tax)
    tax_category_data = response.json()
    yield auth_headers, tax_category_data


@pytest.fixture(scope='module')
def setup_e2e_tax_category(auth_headers):
    created_tax_categories = []

    yield auth_headers, created_tax_categories

    for tax_category in created_tax_categories:
        if 'code' in tax_category:
            try:
                TaxCategoryCall().delete(auth_headers, tax_category['code'])
            except Exception as e:
                print(f"[Cleanup] Error al eliminar tax category {tax_category.get('code')}: {e}")