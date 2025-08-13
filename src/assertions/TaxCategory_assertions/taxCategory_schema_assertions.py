import pytest

from src.assertions.schema_assertions import AssertionSchemas

class AssertionTaxCategory:
    MODULE = "tax_category"

    @staticmethod
    def assert_tax_category_list_schema(response):
        return AssertionSchemas().validate_json_schema(response, "taxCategory_list_schema.json", AssertionTaxCategory.MODULE)

    @staticmethod
    def assert_tax_category_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "taxCategory_add_input_schema.json", AssertionTaxCategory.MODULE)

    @staticmethod
    def assert_tax_category_output_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "taxCategory_add_output_schema.json", AssertionTaxCategory.MODULE)

    @staticmethod
    def assert_tax_category_code_schema(response):
        return AssertionSchemas().validate_json_schema(response, "taxCategory_code_schema.json", AssertionTaxCategory.MODULE)

    @staticmethod
    def assert_tax_category_edit_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "taxCategory_edit_input_schema.json", AssertionTaxCategory.MODULE)

    @staticmethod
    def assert_tax_category_edit_output_schema(response):
        return AssertionSchemas().validate_json_schema(response, "taxCategory_edit_output_schema.json", AssertionTaxCategory.MODULE)