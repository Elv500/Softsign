import pytest

from src.resources.call_request.inventory_call import InventoryCall


@pytest.fixture(scope="function")
def setup_add_inventory(auth_headers):
    created_inventories = []
    yield auth_headers, created_inventories

    for inventory in created_inventories:
        if 'code' in inventory:
            InventoryCall().delete(auth_headers, inventory['code'])
        else:
            print(f"La fuente de inventario no tiene 'code': {inventory}")