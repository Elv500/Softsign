import pytest
from src.assertions.schema_assertions import AssertionSchemas


class AssertionAssociationTypes:
    MODULE = "association_types"

    @staticmethod
    def assert_association_type_add_input_schema(payload):
        """Valida el esquema de entrada para agregar un tipo de asociación"""
        return AssertionSchemas().validate_json_schema(
            payload, "association_type_add_input_schema.json", AssertionAssociationTypes.MODULE
        )

    @staticmethod
    def assert_association_type_add_output_schema(response):
        """Valida el esquema de salida al agregar un tipo de asociación"""
        return AssertionSchemas().validate_json_schema(
            response, "association_type_add_output_schema.json", AssertionAssociationTypes.MODULE
        )

    @staticmethod
    def assert_association_type_add_error_schema(response):
        """Valida el esquema de error al agregar un tipo de asociación"""
        return AssertionSchemas().validate_json_schema(
            response, "association_type_add_error_schema.json", AssertionAssociationTypes.MODULE
        )

    @staticmethod
    def assert_code_matches(response_data, expected_code="EMWPFqAAuwLQHnSjhhdyvfTIhhHSkwuIOpeKpH"):
        """Valida que el código del tipo de asociación coincida con el valor esperado"""
        assert response_data["code"] == expected_code, \
            f"El código no coincide. Esperado: '{expected_code}', Recibido: '{response_data['code']}'"

    @staticmethod
    def assert_translation_name_matches(response_data, locale="en_US", expected_name="cost"):
        """Valida que el nombre de la traducción coincida con el valor esperado"""
        assert locale in response_data["translations"], \
            f"No se encontró la traducción para el idioma '{locale}'"

        actual_name = response_data["translations"][locale]["name"]
        assert actual_name == expected_name, \
            f"El nombre en '{locale}' no coincide. Esperado: '{expected_name}', Recibido: '{actual_name}'"
