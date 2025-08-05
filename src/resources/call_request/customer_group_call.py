from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest

class CustomerGroupCall:
    @classmethod
    def view(cls, headers, customer_group_code):
        """Obtener un customer group específico por código"""
        response = SyliusRequest().get(EndpointCustomerGroup.code(customer_group_code), headers)
        return response.json()
    
    @classmethod
    def create(cls, headers, payload):
        """Crear un nuevo customer group"""
        response = SyliusRequest().post(EndpointCustomerGroup.customer_group(), headers, payload)
        return response.json()
    
    @classmethod
    def update(cls, headers, payload, customer_group_code):
        """Actualizar un customer group existente"""
        response = SyliusRequest().put(EndpointCustomerGroup.code(customer_group_code), headers, payload)
        return response.json()
    
    @classmethod
    def delete(cls, headers, customer_group_code):
        """Eliminar un customer group por código"""
        response = SyliusRequest().delete(EndpointCustomerGroup.code(customer_group_code), headers)
        return response
