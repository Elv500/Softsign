from src.routes.endpoint_tax_category import EndpointTaxCategory
from src.routes.request import SyliusRequest

class TaxCategoryCall:
    @classmethod
    def view(cls, headers, tax_category_code):
        response = SyliusRequest().get(EndpointTaxCategory.code(tax_category_code), headers)
        return response.json()

    @classmethod
    def create(cls, headers, payload):
        response = SyliusRequest().post(EndpointTaxCategory.tax_category(), headers, payload)
        return response.json()

    @classmethod
    def update(cls, headers, payload, tax_category_code):
        response = SyliusRequest().put(EndpointTaxCategory.code(tax_category_code), headers, payload)
        return response.json()

    @classmethod
    def delete(cls, headers, tax_category_code):
        response = SyliusRequest().delete(EndpointTaxCategory.code(tax_category_code), headers)
        return response

    # En TaxCategoryCall
    @classmethod
    def create(cls, headers, payload):
        response = SyliusRequest().post(EndpointTaxCategory.tax_category(), headers, payload)
        return response  # <--- devuelve el objeto Response, NO response.json()