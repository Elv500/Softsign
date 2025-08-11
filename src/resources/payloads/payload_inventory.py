import json

class PayloadInventory:

    @staticmethod
    def build_payload_add_inventory(data):
        payload = {
            "address": {
                "countryCode": data.get("countryCode"),
                "street": data.get("street"),
                "city": data.get("city"),
                "postcode": data.get("postcode")
            },
            "code": data.get("code"),
            "name": data.get("name"),
            "priority": data.get("priority", 0),
            "channels": data.get("channels", [])
        }

        return payload