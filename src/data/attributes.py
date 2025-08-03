from faker import Faker
import json
import uuid
import time

fake = Faker()


def generate_attributes_source_data():
    # Generar un código único combinando timestamp y uuid
    timestamp = str(int(time.time()))[-6:]
    unique_id = str(uuid.uuid4())[:8]  #

    attributes_data = {
        "code": f"test_{timestamp}_{unique_id}",  # Código único garantizado
        "type": "text",  # O el tipo que necesites (text, select, boolean, etc.)
        "translations": {
            "en_US": {
                "name": f"{fake.company()} - {fake.catch_phrase()}"
            }
        }
    }
    return attributes_data



