import pytest

from src.resources.call_request.taxCategory_call import TaxCategoryCall


@pytest.fixture(scope="function")
def setup_add_tax_category(auth_headers):
    created_tax_categories = []
    yield auth_headers, created_tax_categories

    for category in created_tax_categories:
        if 'code' in category:
            TaxCategoryCall().delete(auth_headers, category['code'])
        else:
            print(f"La categoría no tiene 'code': {category}")