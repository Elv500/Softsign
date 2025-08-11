from faker import Faker

fake = Faker()

def generate_inventory_source_data(required_only=False):
    inventory_data = {
        "code": fake.bothify(text='??###'),
        "name": fake.company()
    }

    if not required_only:
        inventory_data["priority"] = fake.random_int(min=0, max=100)
        inventory_data["address"] = {
            "countryCode": fake.country_code(),
            "street": fake.street_address(),
            "city": fake.city(),
            "postcode": fake.postcode()
        }
        inventory_data["channels"] = [
            "/api/v2/admin/channels/HOME_WEB"
        ]

    return inventory_data

def create_inventory_data(address=None, code=None, name=None, priority=None, channels=None):
    inventory_data = {
        "address": address,
        "code": code or fake.bothify(text='??###'),
        "name": name or fake.company(),
        "priority": priority,
        "channels": channels
    }
    inventory_data = {k: (None if v == "null" else v) for k, v in inventory_data.items()}
    inventory_data = {k: v for k, v in inventory_data.items() if v is not None}
    return inventory_data