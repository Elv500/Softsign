import pytest

from src.resources.call_request.customer_group_call import CustomerGroupCall


@pytest.fixture(scope="function")
def setup_add_customer_group(auth_headers):
    """
    Fixture para manejo de customer groups creados durante los tests.
    Proporciona headers de autenticación y una lista para tracking.
    Al finalizar el test, limpia automáticamente todos los grupos creados.
    """
    created_customer_groups = []
    yield auth_headers, created_customer_groups

    # Teardown: eliminar todos los customer groups creados durante el test
    for customer_group in created_customer_groups:
        if 'code' in customer_group:
            try:
                CustomerGroupCall().delete(auth_headers, customer_group['code'])
                print(f" Customer group eliminado: {customer_group['code']}")
            except Exception as e:
                print(f" Error al eliminar customer group {customer_group['code']}: {e}")
        else:
            print(f" El customer group no tiene 'code': {customer_group}")


@pytest.fixture(scope="function")  
def setup_customer_group_cleanup(auth_headers):
    """
    Fixture alternativo para cleanup manual de customer groups.
    Útil cuando necesitas control específico sobre qué grupos eliminar.
    """
    groups_to_cleanup = []
    
    def add_group_for_cleanup(group_code):
        """Agregar un código de grupo para limpieza posterior"""
        groups_to_cleanup.append(group_code)
    
    # Retornar headers y función helper
    yield auth_headers, add_group_for_cleanup
    
    # Teardown: limpiar grupos marcados para eliminación
    for group_code in groups_to_cleanup:
        try:
            CustomerGroupCall().delete(auth_headers, group_code)
            print(f" Customer group limpiado: {group_code}")
        except Exception as e:
            print(f" Error durante cleanup de {group_code}: {e}")
