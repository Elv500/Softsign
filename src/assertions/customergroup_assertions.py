import pytest
from src.assertions.schema_assertions import AssertionSchemas

class AssertionCustomerGroup:

    MODULE = "customer_group"

    @staticmethod
    def assert_customer_group_get_output_schema(response):
        return AssertionSchemas().validate_json_schema(response, "customer_group_get_output_schema.json", AssertionCustomerGroup.MODULE)
    
    @staticmethod
    def assert_customer_group_post_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "customer_group_post_input_schema.json", AssertionCustomerGroup.MODULE)
    
    @staticmethod
    def assert_customer_group_post_output_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "customer_group_post_output_schema.json", AssertionCustomerGroup.MODULE)