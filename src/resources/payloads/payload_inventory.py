class PayloadInventory:

    @staticmethod
    def build_payload_add_inventory(data):
        address = data.get("address", {})
        payload = {
            "address": {
                "countryCode": address.get("countryCode"),
                "street": address.get("street"),
                "city": address.get("city"),
                "postcode": address.get("postcode")
            },
            "code": data.get("code"),
            "name": data.get("name"),
            "priority": data.get("priority", 0),
            "channels": data.get("channels", [])
        }

        return payload