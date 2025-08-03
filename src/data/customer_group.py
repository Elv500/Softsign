from faker import Faker
import json
import uuid
import time

fake = Faker()

def generate_customer_group_source_data():
    # Generar código único combinando timestamp y uuid
    timestamp = str(int(time.time()))[-6:]  # Últimos 6 dígitos del timestamp
    unique_id = str(uuid.uuid4())[:8]  # Primeros 8 caracteres del UUID
    
    customer_group_data = {
        "code": f"test_{timestamp}_{unique_id}",  # Código único garantizado
        "name": f"{fake.company()} - {fake.catch_phrase()}"  # Nombre único
    }
    
    return customer_group_data