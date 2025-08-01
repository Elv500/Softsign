from src.routes.endpoint import Endpoint
from utils.config import BASE_URL

class EndpointInventory:

    @classmethod
    def inventory(cls):
        return f"{BASE_URL}{Endpoint.BASE_INVENTORY.value}"
    
    @staticmethod
    def buil_url_inventory_code(base, inventory_id):
        return f"{BASE_URL}{base.format(inventory_id=inventory_id)}"
    
    @classmethod
    def code(cls, inventory_id):
        return cls.buil_url_inventory_code(Endpoint.BASE_INVENTORY_CODE.value, inventory_id)