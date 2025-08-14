class PayloadOptions:
    """
    Options for payloads.
    """
    @staticmethod
    def build_payload_options(data):
        payload = {
                "code": data.get("code"),
                "name": data.get("name"),
                "translations": {
                    "en_US": {
                        "name": data.get("name"),
                    }
                }
        }
        return payload