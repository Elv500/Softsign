from src.routes.endpoint_product_association import EndpointAssociationTypes
from src.routes.request import SyliusRequest


class AssociationTypesCall:
    @classmethod
    def view(cls, headers, association_type_code):
        response = SyliusRequest().get(
            EndpointAssociationTypes.code(association_type_code), headers)
        return response.json()

    @classmethod
    def create(cls, headers, payload):
        response = SyliusRequest().post(
            EndpointAssociationTypes.association_types(), headers, payload)
        return response.json()

    @classmethod
    def update(cls, headers, payload, association_type_code):
        response = SyliusRequest().put(
            EndpointAssociationTypes.code(association_type_code), headers, payload)
        return response.json()

    @classmethod
    def delete(cls, headers, association_type_code):
        response = SyliusRequest().delete(
            EndpointAssociationTypes.code(association_type_code), headers)
        return response

    @classmethod
    def list(cls, headers, page=1, items_per_page=10, order="asc", translations_name="", code=""):
        url = EndpointAssociationTypes.list(
            page, items_per_page, order, translations_name, code)
        response = SyliusRequest().get(url, headers)
        return response.json()
