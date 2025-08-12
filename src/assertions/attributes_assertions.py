import pytest
from src.assertions.schema_assertions import AssertionSchemas

class AssertionAttributes:

    MODULE = "attributes"

    @staticmethod
    def assert_attributes_get_output_schema(response):
        return AssertionSchemas().validate_json_schema(response, "attributes_get_output_schema.json", AssertionAttributes.MODULE)

    @staticmethod
    def assert_attributes_post_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "attributes_post_input_schema.json", AssertionAttributes.MODULE)

    @staticmethod
    def assert_attributes_post_output_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "attributes_post_output_schema.json", AssertionAttributes.MODULE)

    @staticmethod
    def assert_attributes_list_schema(response):
        return AssertionSchemas().validate_json_schema(response, "attributes_list_schema.json",AssertionAttributes.MODULE)

    @staticmethod
    def assert_attributes_put_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "attributes_put_input_schema.json",AssertionAttributes.MODULE)

    @staticmethod
    def assert_attributes_put_output_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "attributes_put_output_schema.json",AssertionAttributes.MODULE)