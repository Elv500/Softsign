import pytest

class AssertionTaxCategoryFields:

    @staticmethod
    def assert_tax_category_root_metadata(response_json, params=None):
        """Valida la estructura y metadatos del listado de tax categories"""
        try:
            assert response_json["@context"].strip() != "", "Campo '@context' está vacío"
            assert response_json["@id"].strip() != "", "Campo '@id' está vacío"
            assert response_json["@type"].strip() != "", "Campo '@type' está vacío"

            # Validar que hydra:member sea lista y recorrer sus elementos
            members = response_json.get("hydra:member", [])
            assert isinstance(members, list), "'hydra:member' no es una lista"
            if members:
                for item in members:
                    AssertionTaxCategoryFields.assert_tax_category_item_content(item)

            # Validación de paginación si params se especifica
            if params:
                AssertionTaxCategoryFields.assert_tax_category_pagination(response_json, params)
        except AssertionError as e:
            pytest.fail(f"Error en metadatos raíz de Tax Category: {e}")

    @staticmethod
    def assert_tax_category_pagination(response_json, params):
        """Valida que la paginación coincida con los parámetros enviados"""
        try:
            expected_count = params.get("itemsPerPage")
            page = params.get("page", 1)
            if expected_count is not None:
                assert len(response_json["hydra:member"]) == expected_count, \
                    "No coincide la cantidad de elementos solicitada"
                if expected_count == 0:
                    expected_id = f"/api/v2/admin/tax-categories?itemsPerPage={expected_count}"
                else:
                    expected_id = f"/api/v2/admin/tax-categories?itemsPerPage={expected_count}&page={page}"
                assert response_json["hydra:view"]["@id"] == expected_id, \
                    "No coincide: 'hydra:view.@id'"
        except AssertionError as e:
            pytest.fail(f"Error en paginación de Tax Category: {e}")

    @staticmethod
    def assert_tax_category_item_content(item, expected_code=None):
        """Valida la estructura de un objeto tax category"""
        try:
            assert item["@id"].strip() != "", "Campo '@id' en item está vacío"
            assert item["@type"].strip() != "", "Campo '@type' en item está vacío"
            assert item["id"] > 0, "Campo 'id' en item debe ser mayor que 0"

            if expected_code:
                assert item["code"] == expected_code, \
                    f"Código esperado '{expected_code}', encontrado '{item['code']}'"
            else:
                assert item["code"].strip() != "", "Campo 'code' en item está vacío"

            # Cambio aquí: name puede ser None o vacío
            if "name" in item:
                assert item["name"] is not None, "Campo 'name' es None"

            # Resto de validaciones igual...
        except AssertionError as e:
            pytest.fail(f"Error en contenido del item de Tax Category: {e}")