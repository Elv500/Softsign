import pytest


class AssertionCustomerGroupPerformance:

    @staticmethod
    def assert_response_time(elapsed_time, max_time=2.0):
        """Valida que el tiempo de respuesta esté dentro del límite aceptable"""
        try:
            assert elapsed_time < max_time, f"Tiempo de respuesta muy alto: {elapsed_time:.2f}s"
        except AssertionError as e:
            pytest.fail(f"Error en tiempo de respuesta de Customer Group: {e}")

    @staticmethod
    def assert_creation_response_time(elapsed_time, max_time=3.0):
        """Valida que el tiempo de respuesta para creación esté dentro del límite aceptable"""
        try:
            assert elapsed_time < max_time, f"Tiempo de respuesta de creación muy alto: {elapsed_time:.2f}s"
        except AssertionError as e:
            pytest.fail(f"Error en tiempo de respuesta de creación de Customer Group: {e}")

    @staticmethod
    def assert_content_type_header(response_headers, expected_content_type="application/ld+json"):
        """Valida que el Content-Type sea el esperado"""
        try:
            content_type = response_headers.get("Content-Type", "")
            assert content_type.startswith(expected_content_type), \
                f"Content-Type incorrecto: {content_type}"
        except AssertionError as e:
            pytest.fail(f"Error en headers de respuesta de Customer Group: {e}")

    @staticmethod
    def assert_creation_content_type_header(response_headers):
        """Valida que el Content-Type sea el esperado para operaciones de creación"""
        try:
            content_type = response_headers.get("Content-Type", "")
            assert content_type.startswith("application/ld+json"), \
                f"Expected JSON-LD content type, got: {content_type}"
        except AssertionError as e:
            pytest.fail(f"Error en headers de respuesta de creación de Customer Group: {e}")
    
    def assert_update_response_time(self, elapsed_time, max_time=3.0):
        """Verifica que el tiempo de respuesta de actualización esté dentro del límite esperado."""
        assert elapsed_time < max_time, \
            f"Tiempo de respuesta de actualización muy alto: {elapsed_time:.2f}s (máximo: {max_time}s)"
    
    def assert_update_content_type_header(self, response):
        """Verifica que la respuesta de actualización tenga el header Content-Type correcto."""
        headers = response.headers
        content_type = headers.get("Content-Type", "")
        assert content_type.startswith("application/ld+json"), \
            f"Expected JSON-LD content type for update, got: {content_type}"

    @staticmethod
    def assert_pagination_item_limit(response_json, max_items_per_page):
        """Valida que la cantidad de items no exceda el límite solicitado"""
        try:
            member_count = len(response_json["hydra:member"])
            assert member_count <= max_items_per_page, \
                f"Cantidad de items ({member_count}) excede el límite solicitado ({max_items_per_page})"
        except AssertionError as e:
            pytest.fail(f"Error en límite de items por página de Customer Group: {e}")

    @staticmethod
    def assert_multiple_creation_uniqueness(responses):
        """Valida que múltiples creaciones generen códigos únicos"""
        try:
            codes = [resp.json()["code"] for resp in responses]
            assert len(codes) == len(set(codes)), "Los códigos deben ser únicos"
        except AssertionError as e:
            pytest.fail(f"Error en unicidad de códigos en creaciones múltiples de Customer Group: {e}")

    def assert_delete_response_time(self, elapsed_time, max_time=3.0):
        """
        Verifica que el tiempo de respuesta de eliminación esté dentro del límite esperado.
        
        Args:
            elapsed_time (float): Tiempo transcurrido en segundos
            max_time (float): Tiempo máximo permitido en segundos (default: 3.0)
        """
        assert elapsed_time < max_time, \
            f"Tiempo de respuesta de eliminación muy alto: {elapsed_time:.2f}s (máximo: {max_time}s)"
    
    def assert_delete_empty_response(self, response):
        """
        Verifica que la respuesta de eliminación esté vacía (204 No Content).
        
        Args:
            response: Objeto de respuesta HTTP
        """
        assert response.content == b"" or len(response.content) == 0, \
            "Respuesta 204 debe estar vacía"
