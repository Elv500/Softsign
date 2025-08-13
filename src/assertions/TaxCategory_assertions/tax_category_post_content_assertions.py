import pytest

class AssertionTaxCategoryCreate:

    @staticmethod
    def assert_tax_category_payload(payload, required_only=False):
        """Valida que el payload de creación/edición de tax category cumpla con los campos requeridos"""
        try:
            assert payload["code"] != "", "Campo 'code' vacío"
            assert payload["name"] != "", "Campo 'name' vacío"

            # description es opcional, pero si se envía no debe estar vacía
            if not required_only and "description" in payload and payload["description"] is not None:
                assert payload["description"].strip() != "", "Campo 'description' vacío"

        except AssertionError as e:
            pytest.fail(f"Error en el payload de Tax Category: {e}")

    @staticmethod
    def assert_tax_category_response(payload, response_json, required_only=False):
        """Valida que la respuesta de creación/edición de tax category cumpla con lo esperado"""
        try:
            assert response_json["@context"].strip() != "", "Campo '@context' está vacío"
            assert response_json["@id"].strip() != "", "Campo '@id' está vacío"
            assert response_json["@type"].strip() != "", "Campo '@type' está vacío"

            assert response_json["id"] >= 0, "Campo 'id' inválido"
            assert response_json["code"] == payload["code"], f"Código esperado '{payload['code']}', encontrado '{response_json['code']}'"
            assert response_json["name"] == payload["name"], f"Nombre esperado '{payload['name']}', encontrado '{response_json['name']}'"

            # description es opcional, se valida solo si estaba en el payload
            if not required_only and "description" in payload:
                assert response_json["description"] == payload["description"], \
                    f"Descripción esperada '{payload['description']}', encontrada '{response_json['description']}'"

            # Campos obligatorios en output
            assert response_json["createdAt"].strip() != "", "Campo 'createdAt' vacío"
            assert response_json["updatedAt"].strip() != "", "Campo 'updatedAt' vacío"

        except AssertionError as e:
            pytest.fail(f"Error en el response de Tax Category: {e}")
