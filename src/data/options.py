from faker import Faker
import time
fake = Faker()

def generate_options_source_data():
    timestamp = int(time.time())  # Para garantizar unicidad
    unique_id = fake.bothify(text='??##')  # Ej: "AB42"
    options_data = {
        "code": f"test_{timestamp}_{unique_id}",
        "position": fake.random_int(min=0, max=100),
        "translations": {
            "en_US": {
                "name": f"{fake.name()} Option"
            }
        }
    }

    return options_data

def generate_options_source_data_with_values(num_values=1):
    timestamp = int(time.time())
    unique_id = fake.bothify(text='??##')
    values = [
        {
            "code": fake.unique.bothify(text='VAL_##??'),
            "translations": {
                "en_US": {
                    "value": fake.word()
                }
            }
        }
        for _ in range(num_values)
    ]
    return {
        "code": f"test_{timestamp}_{unique_id}",
        "position": fake.random_int(min=0, max=100),
        "values": values,
        "translations": {
            "en_US": {
                "name": fake.word().capitalize()
            }
        }
    }
