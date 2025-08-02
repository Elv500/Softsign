from faker import Faker
from uuid import uuid4
import json

fake = Faker()

def generate_tax_category_source_data():
    taxCategory_data = {
        #generar codigo
        "code": f"TAX-{uuid4().hex[:6]}",
        #nombre de categoria
        "name": fake.word().capitalize(),
        #descripcion
        "description": fake.sentence(nb_words=6),

    }
    return taxCategory_data
