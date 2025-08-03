import json
from faker import Faker
fake = Faker()

class PayloadAttributes:

    @staticmethod
    def build_payload_add_attributes(data):
        payload = {
            "code": data.get("code"),
            "name": data.get("name"),
            "translations": {
                "en_US": {
                    "name": fake.word().capitalize()
                }
            }
        }
        return json.dumps(payload, indent=4)

