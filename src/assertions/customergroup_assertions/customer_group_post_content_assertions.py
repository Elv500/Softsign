import pytest

class AssertionCustomerGroupCreate:

    @staticmethod
    def assert_customer_group_payload(payload, required_only=False):
        """Valida que el payload de creación/edición de customer group cumpla con los campos requeridos"""
        try:
            assert payload["code"] != "", "Campo 'code' vacío"
            assert payload["name"] != "", "Campo 'name' vacío"

            # CustomerGroup no tiene campo 'description' como TaxCategory
            # Solo tiene campos: code, name

        except AssertionError as e:
            pytest.fail(f"Error en el payload de Customer Group: {e}")

    @staticmethod
    def assert_customer_group_response(payload, response_json, required_only=False):
        """Valida que la respuesta de creación/edición de customer group cumpla con lo esperado"""
        try:
            assert response_json["@context"].strip() != "", "Campo '@context' está vacío"
            assert response_json["@id"].strip() != "", "Campo '@id' está vacío"
            assert response_json["@type"].strip() != "", "Campo '@type' está vacío"

            assert response_json["id"] >= 0, "Campo 'id' inválido"
            assert response_json["code"] == payload["code"], f"Código esperado '{payload['code']}', encontrado '{response_json['code']}'"
            assert response_json["name"] == payload["name"], f"Nombre esperado '{payload['name']}', encontrado '{response_json['name']}'"

            # CustomerGroup no tiene campos 'description', 'createdAt', 'updatedAt' como TaxCategory
            # Solo tiene campos en response: @context, @id, @type, id, code, name

        except AssertionError as e:
            pytest.fail(f"Error en el response de Customer Group: {e}")
