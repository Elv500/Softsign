import pytest

class AssertionInventoryFields:

    @staticmethod
    def assert_inventory_root_metadata(response_json, params=None):
        try:
            assert response_json["@context"].strip() != "", "Campo '@context' está vacío"
            assert response_json["@id"].strip() != "", "Campo '@id' está vacío"
            assert response_json["@type"].strip() != "", "Campo '@type' está vacío"
            assert response_json["hydra:totalItems"] >= 0, "'hydra:totalItems' es negativo"
            
            members = response_json.get("hydra:member", [])
            assert isinstance(members, list), "'hydra:member' no es una lista"
            if members:
                for item in members:
                    AssertionInventoryFields.assert_inventory_item_content(item)
            
            if params:
                AssertionInventoryFields.assert_inventory_pagination(response_json, params)
        except AssertionError as e:
            pytest.fail(f"Error en metadatos raíz: {e}")
    
    @staticmethod
    def assert_inventory_pagination(response_json, params):
        try:
            expected_count = params.get("itemsPerPage")
            page = params.get("page", 1)
            if expected_count is not None:
                assert len(response_json["hydra:member"]) == expected_count, "No coincide la cantidad de elementos solicitadas"
                if expected_count == 0:
                    expected_id = f"/api/v2/admin/inventory-sources?itemsPerPage={expected_count}"
                else:
                    expected_id = f"/api/v2/admin/inventory-sources?itemsPerPage={expected_count}&page={page}"
                assert response_json["hydra:view"]["@id"] == expected_id, "No coincide: 'hydra:view.@id'"
        except AssertionError as e:
            pytest.fail(f"Error en mostrar la paginación: {e}")

    @staticmethod
    def assert_inventory_item_content(item, expected_code=None):
        try:
            if "@context" in item:
                assert item["@context"].strip() != "", "Campo '@context' en item está vacío"
            assert item["@id"].strip() != "", "Campo '@id' en item está vacío"
            assert item["@type"].strip() != "", "Campo '@type' en item está vacío"
            assert item["id"] > 0, "Campo 'id' en item debe ser mayor que 0"
            if expected_code:
                assert item["code"] == expected_code, f"Código esperado '{expected_code}', encontrado '{item['code']}'"
            else:
                assert item["code"].strip() != "", "Campo 'code' en item está vacío"
            assert item["name"].strip() != "", "Campo 'name' en item está vacío"
            assert item["priority"] >= 0, "Campo 'priority' en item es negativo"
            if item["channels"]:
                assert all(channel.strip() != "" for channel in item["channels"]), "Algunos canales están vacíos"
        except AssertionError as e:
            pytest.fail(f"Error en contenido del item: {e}")