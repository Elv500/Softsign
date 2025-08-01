#Agregar las assersiones para las esquemas que se encuentran en schemas .json

import pytest
from src.assertions.schema_assertions import AssertionSchemas

class AssertionInventory:

    MODULE = "inventory"

    @staticmethod
    def assert_inventory_list_schema(response):
        return AssertionSchemas().validate_json_schema(response, "inventory_list_schema.json", AssertionInventory.MODULE)
    
    @staticmethod
    def assert_inventory_add_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "inventory_add_input_schema.json", AssertionInventory.MODULE)
    
    @staticmethod
    def assert_inventory_add_output_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "inventory_add_output_schema.json", AssertionInventory.MODULE)