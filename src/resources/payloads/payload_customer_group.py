import json

class PayloadCustomerGroup:

    @staticmethod
    def build_payload_add_customer_group(data):
        payload =  {
        "code": data.get("code"),
        "name": data.get("name")
        }

        return json.dumps(payload, indent=4)
    
    
    