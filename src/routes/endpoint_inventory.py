from src.routes.endpoint import Endpoint
from utils.config import BASE_URL

class EndpointInventory:

    @classmethod
    def inventory(cls):
        return f"{BASE_URL}{Endpoint.BASE_INVENTORY.value}"
    
    @classmethod
    def inventory_with_params(cls, **params):
        """
        Construye URL para inventario con parámetros de consulta opcionales.
        Ejemplo de uso:
            EndpointInventory.inventory_with_params(page=1, itemsPerPage=5)
        """
        base_url = f"{BASE_URL}{Endpoint.BASE_INVENTORY.value}"

        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url

    @staticmethod
    def build_url_inventory_code(base, inventory_code):
        return f"{BASE_URL}{base.format(code=inventory_code)}"
    
    @classmethod
    def code(cls, inventory_code):
        return cls.build_url_inventory_code(Endpoint.BASE_INVENTORY_CODE.value, inventory_code)
