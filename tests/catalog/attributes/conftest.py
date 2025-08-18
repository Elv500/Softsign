import pytest

from src.resources.call_request.attributes_call import AttributesCall


@pytest.fixture(scope="function")
def setup_add_attributes(auth_headers):
    created_attributes = []
    yield auth_headers, created_attributes

    for attributes in created_attributes:
        if 'code' in attributes:
            AttributesCall().delete(auth_headers, attributes['code'])
        else:
            print(f"La fuente de attributes no tiene 'code': {attributes}")


@pytest.fixture(scope="function")
def setup_attributes_cleanup(auth_headers):
    """
    Fixture alternativo para cleanup manual de customer groups.
    Útil cuando necesitas control específico sobre qué grupos eliminar.
    """
    attributes_to_cleanup = []

    def add_attributes_for_cleanup(attributes_code):
        """Agregar un código de grupo para limpieza posterior"""
        attributes_to_cleanup.append(attributes_code)

    # Retornar headers y función helper
    yield auth_headers, add_attributes_for_cleanup

    # Teardown: limpiar grupos marcados para eliminación
    for attributes_code in attributes_to_cleanup:
        try:
            AttributesCall().delete(auth_headers, attributes_code)
            print(f" Attributes limpio: {attributes_code}")
        except Exception as e:
            print(f" Error durante cleanup de {attributes_code}: {e}")