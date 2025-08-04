from faker import Faker
from uuid import uuid4
import re

fake = Faker()

def generate_tax_category_data(
    code=None, name=None, description=None
):
    """
    aqui estamos generando un diccionario de datos validos / aunque permite sobre escribir cualquier campo
    """
    data = {
        "code": code if code is not None else f"TAX-{uuid4().hex[:6]}",
        "name": name if name is not None else fake.word().capitalize(),
        "description": description if description is not None else fake.sentence(nb_words=6),
    }
    return data


def build_invalid_tax_category_data():
    """
    Retorna una lista de diccionarios con combinaciones de datos inválidos para casos negativos.
    """
    invalid_cases = [
        # Code muy largo
        {"code": "A" * 256, "name": "ValidName"},
        # Code con caracteres no permitidos
        {"code": "Abc$", "name": "ValidName"},
        {"code": "TAX#123", "name": "ValidName"},
        # Name muy corto
        {"code": "TAX-123", "name": "A"},
        {"code": "TAX-123", "name": ""},
        # Name muy largo
        {"code": "TAX-123", "name": "A" * 256},
        # Falta code
        {"name": "ValidName"},
        # Falta name
        {"code": "TAX-123"},
        # Description como null (válido)
        {"code": "TAX-123", "name": "ValidName", "description": None},
        # Description muy larga (si hay limitación, agregar aquí)
    ]
    return invalid_cases
