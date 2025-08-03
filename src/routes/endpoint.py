from enum import Enum
from utils.config import BASE_URL

class Endpoint(Enum):
    
    LOGIN = "/administrators/token"
    
    BASE_INVENTORY = "/admin/inventory-sources"
    BASE_INVENTORY_CODE = "/admin/inventory-sources/{code}"
  
    BASE_CUSTOMER_GROUP = "/admin/customer-groups"
    BASE_CUSTOMER_GROUP_CODE = "/admin/customer-groups/{code}"

    @classmethod
    def login(cls):
        return f"{BASE_URL}{cls.LOGIN.value}"