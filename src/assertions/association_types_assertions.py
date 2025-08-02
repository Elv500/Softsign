
import pytest
from src.assertions.schema_assertions import AssertionSchemas


class AssertionAssociationTypes:
    MODULE = "association_types"

    @staticmethod
    def assert_association_types_list_schema(response):
        """Valida el esquema de la lista de tipos de asociación de productos"""
        return AssertionSchemas().validate_json_schema(response, "association_types_list.json", AssertionAssociationTypes.MODULE)

    @staticmethod
    def assert_error_schema(response):
        """Valida que la respuesta de error cumpla con el esquema JSON esperado"""
        AssertionSchemas().validate_json_schema(
            response, "error_response.json", AssertionAssociationTypes.MODULE)

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

    @staticmethod
    def assert_items_per_page_limit(members, expected_limit):
        """Valida que la cantidad de items no exceda el límite por página """
        assert len(members) <= expected_limit, \
            f"La cantidad de items ({len(members)}) excede el límite por página ({expected_limit})"

    @staticmethod
    def assert_total_items_limit(response_data, expected_limit):
        """Valida que la cantidad total de items no exceda el límite esperado"""
        assert response_data["hydra:totalItems"] <= expected_limit, \
            f"La cantidad total de items ({response_data['hydra:totalItems']}) excede el límite esperado ({expected_limit})"

    @staticmethod
    def assert_error_message(response_data, expected_message):
        """Valida que el mensaje de error coincida con el esperado"""
        assert response_data["hydra:description"] == expected_message, \
            f"El mensaje de error no coincide. Esperado: '{expected_message}', Recibido: '{response_data['hydra:description']}'"

    @staticmethod
    def assert_member_count(hydra_member, expected_count):
        actual_count = len(hydra_member)
        assert actual_count == expected_count, \
            f"La cantidad de elementos no coincide. Esperado: {expected_count}, Actual: {actual_count}"

    @staticmethod
    def assert_list_ordered_by_code(member_list, order="asc"):
        """
        Valida que la lista esté ordenada por el campo code sin distinguir entre mayúsculas y minúsculas
        """
        assert len(member_list) > 0, "La lista está vacía, no se puede validar el orden"

        codes = [item["code"] for item in member_list]
        
        sorted_codes = sorted(codes, 
                            key=str.lower,  
                            reverse=(order == "desc"))
        
        assert codes == sorted_codes, \
            f"La lista no está ordenada {order}endentemente por code. " \
            f"Orden actual: {codes}, Orden esperado: {sorted_codes}"
