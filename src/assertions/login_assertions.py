import pytest
from src.assertions.schema_assertions import AssertionSchemas

class AssertionLogin:
     
    MODULE = "login"

    @staticmethod
    def assert_login_input_schema(response):
          return AssertionSchemas().validate_json_schema(response, "login_input_schema.json", AssertionLogin.MODULE)
    
    @staticmethod
    def assert_login_output_schema(response):
         return AssertionSchemas().validate_json_schema(response, "login_output_schema.json", AssertionLogin.MODULE)