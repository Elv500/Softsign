import pytest

class AssertionInventoryErrors:

    @staticmethod
    def assert_inventory_errors(response_json, code, message):
        try:
            assert "code" in response_json, "'code' no está en la respuesta"
            assert "message" in response_json, "'message' no está en la respuesta"
            assert response_json["code"] == code, "Error code no coincide"
            assert response_json["message"] == message, "Error message no coincide"
        except AssertionError as e:
            pytest.fail(f"Mensajes de error erroneos: {e}")

    @staticmethod
    def assert_inventory_error_request(response_json, status, detail):
        try:
            #assert response_json.get("@type") == "hydra:Error", "'@type' no es 'hydra:Error'"
            assert "status" in response_json, "'status' no está en la respuesta"
            assert "detail" in response_json, "'detail' no está en la respuesta"
            assert response_json["status"] == status, "Error status no coincide"
            assert response_json["detail"] == detail, "Error detail no coincide"
        except AssertionError as e:
            pytest.fail(f"Mensajes de error del request erroneos: {e}")