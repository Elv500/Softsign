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
