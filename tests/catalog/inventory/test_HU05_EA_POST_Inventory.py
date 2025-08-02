import pytest
import requests
from faker import Faker

from utils.config import BASE_URL
from src.assertions.inventory_assertions import AssertionInventory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.data.inventory import generate_inventory_source_data

faker = Faker()

@pytest.mark.smoke
def test_TC27_Crear_una_fuente_de_inventario_con_datos_validos(auth_headers):
    
    url = f"{BASE_URL}/admin/inventory-sources"
    data = generate_inventory_source_data()
    response = requests.post(url, headers=auth_headers, json=data)
    AssertionInventory.assert_inventory_add_input_schema(data)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionInventory.assert_inventory_add_output_schema(response.json())
