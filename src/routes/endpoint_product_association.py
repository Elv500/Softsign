from src.routes.endpoint import Endpoint
from utils.config import BASE_URL


class EndpointAssociationTypes:

    @classmethod
    def association_types(cls):
        return f"{BASE_URL}{Endpoint.BASE_ASSOCIATION_TYPES.value}"

    @staticmethod
    def build_url_association_types_code(base, association_code):
        return f"{BASE_URL}{base.format(code=association_code)}"

    @classmethod
    def code(cls, association_code):
        return cls.build_url_association_types_code(Endpoint.BASE_ASSOCIATION_TYPES_CODE.value, association_code)

    @staticmethod
    def build_url_association_types_list(base, page=1, items_per_page=10, order="asc", translations_name="", code=""):
        url = (
            f"{BASE_URL}{base}"
            f"?page={page}"
            f"&itemsPerPage={items_per_page}"
            f"&order[code]={order}"
        )
        if translations_name:
            url += f"&translations.name={translations_name}"
        if code:
            url += f"&code={code}"
        return url

    @classmethod
    def list(cls, page=1, items_per_page=10, order="asc", translations_name="", code=""):
        return cls.build_url_association_types_list(
            Endpoint.BASE_ASSOCIATION_TYPES.value, page, items_per_page, order, translations_name, code
        )