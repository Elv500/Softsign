from enum import Enum
from utils.config import BASE_URL

class Endpoint(Enum):
    
    LOGIN = "/administrators/token"
    
    BASE_INVENTORY = "/admin/inventory-sources"
    BASE_INVENTORY_CODE = "/admin/inventory-sources/{code}"

    @classmethod
    def login(cls):
        return f"{BASE_URL}{cls.LOGIN.value}"