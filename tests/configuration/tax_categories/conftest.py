import pytest

from src.resources.call_request.taxCategory_call import TaxCategoryCall
from src.resources.payloads.payload_taxCategory import PayloadTaxCategory
from src.data.taxCategory import generate_tax_category_data

@pytest.fixture(scope="module")
def setup_teardown_view_tax_category(auth_headers):
    payload_tax1 = PayloadTaxCategory.build_payload_tax_category(generate_tax_category_data())
    payload_tax2 = PayloadTaxCategory.build_payload_tax_category(generate_tax_category_data())

    # Crear categorías y extraer datos JSON
    response1 = TaxCategoryCall.create(auth_headers, payload_tax1)
    response2 = TaxCategoryCall.create(auth_headers, payload_tax2)
    tax_category1_data = response1.json()
    tax_category2_data = response2.json()

    yield auth_headers, tax_category1_data, tax_category2_data

    # Eliminar usando los datos ya extraídos
    TaxCategoryCall().delete(auth_headers, tax_category1_data['code'])
    TaxCategoryCall().delete(auth_headers, tax_category2_data['code'])

@pytest.fixture(scope="function")
def setup_add_tax_category(auth_headers):
    created_tax_categories = []
    yield auth_headers, created_tax_categories

    for category in created_tax_categories:
        if isinstance(category, dict) and 'code' in category:
            TaxCategoryCall().delete(auth_headers, category['code'])
        elif isinstance(category, str):
            TaxCategoryCall().delete(auth_headers, category)
        else:
            try:
                category_data = category.json()
                TaxCategoryCall().delete(auth_headers, category_data['code'])
            except:
                print(f"No se pudo eliminar la categoría: {category}")

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