from faker import Faker

fake = Faker()

def generate_login_source_data():
    login_data = {
        "email": fake.email(),
        "password": fake.password()
    }

    return login_data