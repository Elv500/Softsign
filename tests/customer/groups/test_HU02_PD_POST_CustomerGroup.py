import jsonschema
import requests
import pytest
import time
from faker import Faker


from src.assertions.customergroup_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from utils.config import BASE_URL
from src.data.customer_group import generate_customer_group_source_data



# Admin > Customer - Group > TC_114 Verificar estructura del JSON devuelto
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC114_Estructura_JSON(auth_headers):
    url = f"{BASE_URL}/admin/customer-groups"
    data = generate_customer_group_source_data()
    print("Generated Customer Group Data:", data)
    response = requests.post(url, json=data, headers=auth_headers)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionCustomerGroup.assert_customer_group_post_output_schema(response.json())


