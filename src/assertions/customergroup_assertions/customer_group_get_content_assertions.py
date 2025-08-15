import pytest


class AssertionCustomerGroupFields:

    @staticmethod
    def assert_customer_group_root_metadata(response_json, params=None):
        """Valida la estructura y metadatos del listado de customer groups"""
        try:
            assert response_json["@context"].strip() != "", "Campo '@context' está vacío"
            assert response_json["@id"].strip() != "", "Campo '@id' está vacío"
            assert response_json["@type"].strip() != "", "Campo '@type' está vacío"

            # Validar que hydra:member sea lista y recorrer sus elementos
            members = response_json.get("hydra:member", [])
            assert isinstance(members, list), "'hydra:member' no es una lista"
            if members:
                for item in members:
                    AssertionCustomerGroupFields.assert_customer_group_item_content(item)

            # Validación de paginación si params se especifica
            if params:
                AssertionCustomerGroupFields.assert_customer_group_pagination(response_json, params)
        except AssertionError as e:
            pytest.fail(f"Error en metadatos raíz de Customer Group: {e}")

    @staticmethod
    def assert_customer_group_pagination(response_json, params):
        """Valida que la paginación coincida con los parámetros enviados"""
        try:
            expected_count = params.get("itemsPerPage")
            page = params.get("page", 1)
            if expected_count is not None:
                assert len(response_json["hydra:member"]) == expected_count, \
                    "No coincide la cantidad de elementos solicitada"
                
                # Construir las posibles URLs esperadas
                if expected_count == 0:
                    expected_ids = [f"/api/v2/admin/customer-groups?itemsPerPage={expected_count}"]
                else:
                    # Algunas APIs incluyen page=1 explícitamente, otras no
                    if page == 1:
                        expected_ids = [
                            f"/api/v2/admin/customer-groups?itemsPerPage={expected_count}",
                            f"/api/v2/admin/customer-groups?itemsPerPage={expected_count}&page={page}"
                        ]
                    else:
                        expected_ids = [f"/api/v2/admin/customer-groups?itemsPerPage={expected_count}&page={page}"]
                
                actual_id = response_json["hydra:view"]["@id"]
                assert actual_id in expected_ids, \
                    f"No coincide: 'hydra:view.@id'. Expected one of: {expected_ids}, Actual: {actual_id}"
        except AssertionError as e:
            pytest.fail(f"Error en paginación de Customer Group: {e}")

    @staticmethod
    def assert_customer_group_item_content(item, expected_code=None):
        """Valida la estructura de un objeto customer group"""
        try:
            assert item["@id"].strip() != "", "Campo '@id' en item está vacío"
            assert item["@type"].strip() != "", "Campo '@type' en item está vacío"
            assert item["id"] > 0, "Campo 'id' en item debe ser mayor que 0"

            if expected_code:
                assert item["code"] == expected_code, \
                    f"Código esperado '{expected_code}', encontrado '{item['code']}'"
            else:
                assert item["code"].strip() != "", "Campo 'code' en item está vacío"

            assert item["name"].strip() != "", "Campo 'name' en item está vacío"

            # Note: CustomerGroup no tiene campo 'description' como TaxCategory
            # CustomerGroup solo tiene: @id, @type, id, code, name

        except AssertionError as e:
            pytest.fail(f"Error en contenido del item de Customer Group: {e}")

    @staticmethod
    def assert_customer_groups_exist(response_json):
        """Valida que exista al menos un grupo de clientes"""
        try:
            grupos = response_json.get("hydra:member", [])
            assert len(grupos) > 0, "Debe existir al menos un grupo"
        except AssertionError as e:
            pytest.fail(f"Error en existencia de Customer Groups: {e}")

    @staticmethod
    def assert_pagination_out_of_range(response_json):
        """Valida que páginas fuera de rango retornen lista vacía"""
        try:
            data = response_json
            member_count = len(data.get("hydra:member", []))
            
            assert isinstance(data.get("hydra:member", []), list)
            assert member_count == 0, "Página fuera de rango debería retornar lista vacía"
        except AssertionError as e:
            pytest.fail(f"Error en paginación fuera de rango de Customer Group: {e}")

    @staticmethod
    def assert_customer_groups_uniqueness(response_json):
        """Valida que los IDs y códigos sean únicos"""
        try:
            grupos = response_json.get("hydra:member", [])
            
            ids = [g["id"] for g in grupos]
            codes = [g["code"] for g in grupos]
            
            assert len(ids) == len(set(ids)), "Los IDs deben ser únicos"
            assert len(codes) == len(set(codes)), "Los códigos deben ser únicos"
        except AssertionError as e:
            pytest.fail(f"Error en unicidad de Customer Groups: {e}")

    @staticmethod
    def assert_customer_groups_field_length_limits(response_json):
        """Valida que los campos respeten los límites de longitud"""
        try:
            grupos = response_json.get("hydra:member", [])
            
            max_code_length = 0
            max_name_length = 0
            
            for grupo in grupos:
                AssertionCustomerGroupFields.assert_customer_group_item_content(grupo)
                
                code_length = len(grupo["code"])
                name_length = len(grupo["name"])
                
                if code_length > max_code_length:
                    max_code_length = code_length
                if name_length > max_name_length:
                    max_name_length = name_length
                    
                assert code_length <= 255, f"Código muy largo: {grupo['code']}"
                assert name_length <= 255, f"Nombre muy largo: {grupo['name']}"
        except AssertionError as e:
            pytest.fail(f"Error en límites de longitud de Customer Groups: {e}")
