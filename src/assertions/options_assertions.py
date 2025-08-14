from src.assertions.schema_assertions import AssertionSchemas


class AssertionOptions:
    MODULE = "Options"

    @staticmethod
    def assert_options_list_schema(response):
        return AssertionSchemas().validate_json_schema(response, "options_get_output_schema.json", AssertionOptions.MODULE)

    @staticmethod
    def assert_options_add_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "options_add_input_schema.json", AssertionOptions.MODULE)

    @staticmethod
    def assert_options_add_output_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "options_add_output_schema.json", AssertionOptions.MODULE)

    @staticmethod
    def assert_options_put_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "options_edit_input_schema.json", AssertionOptions.MODULE)

    @staticmethod
    def assert_options_put_output_schema(response):
        return AssertionSchemas().validate_json_schema(response, "options_edit_output_schema.json", AssertionOptions.MODULE)

    @staticmethod
    def assert_options_code_schema(response):
        return AssertionSchemas().validate_json_schema(response, "options_add_output_schema.json",
                                                       AssertionOptions.MODULE)