from src.routes.endpoint_inventory import EndpointInventory
from src.routes.request import SyliusRequest

class InventoryCall:
    @classmethod
    def view(cls, headers, inventory_code):
        response = SyliusRequest().get(EndpointInventory.code(inventory_code), headers)
        return response.json()
    
    @classmethod
    def create(cls, headers, payload):
        response = SyliusRequest().post(EndpointInventory.inventory(), headers, payload)
        return response.json()
    
    @classmethod
    def update(cls, headers, payload, inventory_code):
        response = SyliusRequest().put(EndpointInventory.code(inventory_code), headers, payload)
        return response.json()
    
    @classmethod
    def delete(cls, headers, inventory_code):
        response = SyliusRequest().delete(EndpointInventory.code(inventory_code), headers)
        return response