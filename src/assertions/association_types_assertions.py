
import pytest
from src.assertions.schema_assertions import AssertionSchemas


class AssertionAssociationTypes:
    MODULE = "association_types"

    @staticmethod
    def assert_association_types_list_schema(response):
        """Valida el esquema de la lista de tipos de asociación de productos"""
        return AssertionSchemas().validate_json_schema(response, "association_types_list.json", AssertionAssociationTypes.MODULE)

    @staticmethod
    def assert_response_has_items(response_data):
        """Valida que haya items en la respuesta"""
        assert response_data["hydra:totalItems"] > 0, "No hay items en la respuesta"
        assert len(response_data["hydra:member"]
                   ) > 0, "La lista de miembros está vacía"

    @staticmethod
    def assert_data_types(member):
        """Valida los tipos de datos de los campos"""
        type_validations = {
            "id": (int, "debe ser un entero"),
            "code": (str, "debe ser una cadena"),
            "name": (str, "debe ser una cadena"),
            "translations": (dict, "debe ser un objeto")
        }

        for field, (expected_type, message) in type_validations.items():
            assert isinstance(member[field], expected_type), \
                f"El campo '{field}' {message}"
