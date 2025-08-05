import json


class PayloadTaxCategory:

    @staticmethod
    def build_payload_tax_category(data):
        payload = {
            "code": data.get("code"),
            "name": data.get("name"),
            "description": data.get("description")
        }
        return payload