from src.routes.endpoint import Endpoint
from utils.config import BASE_URL

class EndpointCustomerGroup:

    @classmethod
    def customer_group(cls):
        return f"{BASE_URL}{Endpoint.BASE_CUSTOMER_GROUP.value}"
    
    @classmethod
    def customer_group_with_params(cls, **params):
        """
        Construye URL con parámetros de consulta (query parameters)
        Ejemplo: customer_group_with_params(page=1, itemsPerPage=2)
        """
        base_url = f"{BASE_URL}{Endpoint.BASE_CUSTOMER_GROUP.value}"
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url
    
    @staticmethod
    def build_url_customer_group_code(base, customer_group_code):
        return f"{BASE_URL}{base.format(code=customer_group_code)}"
    
    @classmethod
    def code(cls, customer_group_code):
        return cls.build_url_customer_group_code(Endpoint.BASE_CUSTOMER_GROUP_CODE.value, customer_group_code)