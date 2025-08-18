from src.routes.endpoint import Endpoint
from utils.config import BASE_URL


class EndpointAttributes:

    @classmethod
    def attributes(cls):
        return f"{BASE_URL}{Endpoint.BASE_ATTRIBUTES.value}"

    @classmethod
    def attributes_with_params(cls, **params):
        """
        Construye URL con query parameters
        Ejemplo: attributes_with_params(page=1)
        """
        base_url = f"{BASE_URL}{Endpoint.BASE_ATTRIBUTES.value}"

        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url

    @staticmethod
    def build_url_attributes_code(base, attributes_code):
        return f"{BASE_URL}{base.format(code=attributes_code)}"

    @classmethod
    def code(cls, attributes_code):
        return cls.build_url_attributes_code(Endpoint.BASE_ATTRIBUTES_CODE.value, attributes_code)