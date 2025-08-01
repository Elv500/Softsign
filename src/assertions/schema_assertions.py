from utils.load_resources import load_schema_resource
import jsonschema
import pytest
import json


class AssertionSchemas:
    @staticmethod
    def validate_json_schema(response, schema_file, module=None):
        try:
            schema = load_schema_resource(schema_file, module)
        except FileNotFoundError:
            pytest.fail(f"Schema file '{schema_file}' not found")
        except json.JSONDecodeError as err:
            pytest.fail(f"Failed to decode JSON schema: {err}")

        try:
            jsonschema.validate(instance=response, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            pytest.fail(f"JSON schema validation failed: {err}")