import pytest
import json

from src.resources.call_request.inventory_call import InventoryCall
from src.resources.payloads.payload_inventory import PayloadInventory
from src.data.inventory import generate_inventory_source_data

@pytest.fixture(scope="module")
def setup_teardown_view_inventory(auth_headers):
    payload_inventory1 = PayloadInventory.build_payload_add_inventory(generate_inventory_source_data())
    payload_inventory2 = PayloadInventory.build_payload_add_inventory(generate_inventory_source_data())
    inventory1 = InventoryCall.create(auth_headers, payload_inventory1)
    inventory2 = InventoryCall.create(auth_headers, payload_inventory2)

    yield auth_headers, inventory1, inventory2

    InventoryCall().delete(auth_headers, inventory1['code'])
    InventoryCall().delete(auth_headers, inventory2['code'])

@pytest.fixture(scope="function")
def setup_add_inventory(auth_headers):
    created_inventories = []
    yield auth_headers, created_inventories

    for inventory in created_inventories:
        if 'code' in inventory:
            InventoryCall().delete(auth_headers, inventory['code'])
        else:
            print(f"La fuente de inventario no tiene 'code': {inventory}")

@pytest.fixture(scope="class")
def setup_edit_inventory(auth_headers):
    payload_inventory = PayloadInventory.build_payload_add_inventory(generate_inventory_source_data())
    inventory = InventoryCall.create(auth_headers, payload_inventory)

    yield auth_headers, inventory

    InventoryCall.delete(auth_headers, inventory["code"])