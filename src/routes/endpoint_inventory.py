from src.routes.endpoint import Endpoint
from utils.config import BASE_URL

class EndpointInventory:

    @classmethod
    def inventory(cls):
        return f"{BASE_URL}{Endpoint.BASE_INVENTORY.value}"
    
    @staticmethod
    def build_url_inventory_code(base, inventory_code):
        return f"{BASE_URL}{base.format(code=inventory_code)}"
    
    @classmethod
    def code(cls, inventory_code):
        return cls.build_url_inventory_code(Endpoint.BASE_INVENTORY_CODE.value, inventory_code)