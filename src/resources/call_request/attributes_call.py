from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest


class AttributesCall:
    @classmethod
    def view(cls, headers, attributes_code):
        response = SyliusRequest().get(EndpointAttributes.code(attributes_code), headers)
        return response.json()

    @classmethod
    def create(cls, headers, payload):
        response = SyliusRequest().post(EndpointAttributes.attributes(), headers, payload)
        return response.json()

    @classmethod
    def update(cls, headers, payload, attribute_code):
        response = SyliusRequest().put(EndpointAttributes.code(attribute_code), headers, payload)
        return response.json()

    @classmethod
    def delete(cls, headers, attribute_code):
        response = SyliusRequest().delete(EndpointAttributes.code(attribute_code), headers)
        return response