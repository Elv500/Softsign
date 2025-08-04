from enum import Enum
from utils.config import BASE_URL


class Endpoint(Enum):

    LOGIN = "/admin/administrators/token"

    BASE_INVENTORY = "/admin/inventory-sources"
    BASE_INVENTORY_CODE = "/admin/inventory-sources/{code}"

    BASE_CUSTOMER_GROUP = "/admin/customer-groups"
    BASE_CUSTOMER_GROUP_CODE = "/admin/customer-groups/{code}"

    BASE_ATTRIBUTES = "/admin/product-attributes"
    BASE_ATTRIBUTES_CODE = "/admin/product-attributes/{code}"

    BASE_OPTIONS = "/admin/product-options"
    BASE_OPTIONS_CODE = "/admin/product-options/{code}"

    BASE_ASSOCIATION_TYPES = "/admin/product-association-types"
    BASE_ASSOCIATION_TYPES_CODE = "/admin/product-association-types/{code}"

    @classmethod
    def login(cls):
        return f"{BASE_URL}{cls.LOGIN.value}"
