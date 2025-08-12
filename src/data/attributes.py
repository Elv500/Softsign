import uuid

from faker import Faker
import json
import uuid
import time

fake = Faker()

def generate_attributes_source_data(required_only=False):
    code = fake.unique.slug()
    name = fake.unique.company()
    payload = {
        "code": code,
        "type": "text",
        "translations": {
            "en_US": {
                "name": name
            }
        },
        "configuration": {
            "maxCharacters": fake.random_int(min=10, max=200),
            "minCharacters": fake.random_int(min=1, max=10)
        },
        "storageType": "text"
    }
    return payload
