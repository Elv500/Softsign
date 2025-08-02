import json

class PayloadLogin:

    @staticmethod
    def build_payload_login(data):
        payload = {
            "email": data.get("email"),
            "password": data.get("password")
        }

        return json.dumps(payload, indent=4)