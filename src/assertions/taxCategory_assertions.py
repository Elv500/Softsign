import pytest

from src.assertions.schema_assertions import AssertionSchemas

class AssertionTaxCategory:
    MODULE = "tax_category"

    @staticmethod
    def assert_tax_category_list_schema(response):
        return AssertionSchemas().validate_json_schema(response, "taxCategory_list_schema.json", AssertionTaxCategory.MODULE)
