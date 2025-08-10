from src.routes.endpoint_options import EndpointOptions
from src.routes.request import SyliusRequest

class OptionsCall:
    @classmethod
    def view(cls, headers):
        """Obtener las opciones disponibles"""
        response = SyliusRequest().get(EndpointOptions.options(), headers)
        return response.json()

    @classmethod
    def create(cls, headers, payload):
        """Crear una nueva opción"""
        response = SyliusRequest().post(EndpointOptions.options(), headers, payload)
        return response.json()

    @classmethod
    def update(cls, headers, payload, option_code):
        """Actualizar una opción existente"""
        response = SyliusRequest().put(EndpointOptions.code(option_code), headers, payload)
        return response.json()

    @classmethod
    def delete(cls, headers, option_code):
        """Eliminar una opción por código"""
        response = SyliusRequest().delete(EndpointOptions.code(option_code), headers)
        return response

    @classmethod
    def view_option(cls, headers, option_code):
        """Obtener una opción específica por código"""
        response = SyliusRequest().get(EndpointOptions.code(option_code), headers)
        return response.json() if response.status_code == 200 else None
