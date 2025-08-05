from faker import Faker

fake = Faker()

def generate_inventory_source_data(required_only=False):
    inventory_data = {
        "code": fake.bothify(text='??###'),
        "name": fake.company(),
        "priority": fake.random_int(min=0, max=100),
    }

    if not required_only:
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