from enum import Enum
from utils.config import BASE_URL


class Endpoint(Enum):

    LOGIN = "/api/v2/admin/administrators/token"

    BASE_INVENTORY = "/api/v2/admin/inventory-sources"
    BASE_INVENTORY_CODE = "/api/v2/admin/inventory-sources/{code}"

    BASE_CUSTOMER_GROUP = "/api/v2/admin/customer-groups"
    BASE_CUSTOMER_GROUP_CODE = "/api/v2/admin/customer-groups/{code}"

    BASE_TAX_CATEGORY = "/api/v2/admin/tax-categories"
    BASE_TAX_CATEGORY_CODE = "/api/v2/admin/tax-categories/{code}"

    BASE_ATTRIBUTES = "/api/v2/admin/product-attributes"
    BASE_ATTRIBUTES_CODE = "/api/v2/admin/product-attributes/{code}"

    BASE_OPTIONS = "/api/v2/admin/product-options"
    BASE_OPTIONS_CODE = "/api/v2/admin/product-options/{code}"

    BASE_ASSOCIATION_TYPES = "/api/v2/admin/product-association-types"
    BASE_ASSOCIATION_TYPES_CODE = "/api/v2/admin/product-association-types/{code}"

    @classmethod
    def login(cls):
        return f"{BASE_URL}{cls.LOGIN.value}"