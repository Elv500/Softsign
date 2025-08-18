from src.routes.endpoint import Endpoint
from utils.config import BASE_URL


class EndpointOptions:

    @classmethod
    def options(cls):
        return f"{BASE_URL}{Endpoint.BASE_OPTIONS.value}"

    @staticmethod
    def build_url_options_code(base, options_code):
        return f"{BASE_URL}{base.format(code=options_code)}"

    @classmethod
    def code(cls, options_code):
        return cls.build_url_options_code(Endpoint.BASE_OPTIONS_CODE.value, options_code)

    @classmethod
    def options_with_params(cls, **params):
        """
        Construye URL para inventario con parámetros de consulta opcionales.
        Ejemplo de uso:
            EndpointInventory.inventory_with_params(page=1, itemsPerPage=5)
        """
        base_url = f"{BASE_URL}{Endpoint.BASE_OPTIONS.value}"

        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url
