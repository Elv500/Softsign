from faker import Faker

fake = Faker()

def generate_inventory_source_data():
    inventory_data = {
        "address": {
            "countryCode": fake.country_code(),    # Código país tipo "US", "GB", etc.
            "street": fake.street_address(),
            "city": fake.city(),
            "postcode": fake.postcode()
        },
        "code": fake.bothify(text='??###'),       # Código aleatorio tipo "AB123"
        "name": fake.company(),
        "priority": fake.random_int(min=0, max=10),
        "channels": [
            "/api/v2/admin/channels/HOME_WEB"
        ]
    }
    #return json.dumps(inventory_data, indent=4)
    return inventory_data