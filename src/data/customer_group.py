from faker import Faker
import json

fake = Faker()

def generate_customer_group_source_data():
    customer_group_data = {
        "code": fake.numerify(),
        "name": fake.company()
        }
    
    #return json.dumps(inventory_data, indent=4)
    return customer_group_data