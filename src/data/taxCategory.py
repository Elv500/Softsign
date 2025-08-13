from faker import Faker
from uuid import uuid4

fake = Faker()


def generate_tax_category_data(required_only=False):
    tax_category_data = {
        "code": f"TAX-{uuid4().hex[:6]}",
        "name": fake.word().capitalize()
    }

    if not required_only:
        tax_category_data["description"] = fake.sentence(nb_words=6)

    # Validar que los campos requeridos no sean None
    assert tax_category_data["code"] is not None, "El código no puede ser None"
    assert tax_category_data["name"] is not None, "El nombre no puede ser None"

    return tax_category_data


def create_tax_category_data(code=None, name=None, description=None):
    """
    Crea un diccionario de Tax Category con valores personalizados o aleatorios.
    """
    tax_category_data = {
        "code": code or f"TAX-{uuid4().hex[:6]}",
        "name": name or fake.word().capitalize(),
        "description": description
    }

    # Convierte valores "null" en None
    tax_category_data = {k: (None if v == "null" else v) for k, v in tax_category_data.items()}

    # Elimina las claves cuyo valor sea None
    tax_category_data = {k: v for k, v in tax_category_data.items() if v is not None}

    return tax_category_data
