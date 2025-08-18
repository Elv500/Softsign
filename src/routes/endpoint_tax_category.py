import urllib.parse
from src.routes.endpoint import Endpoint
from utils.config import BASE_URL

class EndpointTaxCategory:

    @classmethod
    def tax_category(cls):
        return f"{BASE_URL}{Endpoint.BASE_TAX_CATEGORY.value}"

    @classmethod
    def tax_category_with_params(cls, **params):
        base_url = f"{BASE_URL}{Endpoint.BASE_TAX_CATEGORY.value}"
        if params:
            query_string = urllib.parse.urlencode(params)
            return f"{base_url}?{query_string}"
        return base_url

    @staticmethod
    def build_url_tax_category(base, tax_category_code):
        return f"{BASE_URL}{base.format(code=tax_category_code)}"

    @classmethod
    def code(cls, tax_category_code):
        return cls.build_url_tax_category(Endpoint.BASE_TAX_CATEGORY_CODE.value, tax_category_code)