import pytest

from src.assertions.customergroup_assertions.customer_group_schema_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from src.data.customer_group import generate_customer_group_source_data
from utils.logger_helpers import log_request_response

# Admin > Customer - Group > TC_334 E2E: Flujo completo CRUD de grupo de clientes
@pytest.mark.e2e
@pytest.mark.customer_group
def test_TC334_e2e_customer_group(auth_headers):
    
    # POST
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    
    log_request_response(create_endpoint, create_response, headers=auth_headers)
    
    created_group = create_response.json()
    customer_group_code = created_group["code"]
    
    # GET
    get_endpoint = EndpointCustomerGroup.code(customer_group_code)
    get_response = SyliusRequest.get(get_endpoint, auth_headers)
    
    log_request_response(get_endpoint, get_response, headers=auth_headers)
    
    # PUT
    updated_data = {
        "code": customer_group_code,
        "name": f"UPDATED - {initial_data['name']} - E2E Test"
    }
    
    put_endpoint = EndpointCustomerGroup.code(customer_group_code)
    put_response = SyliusRequest.put(put_endpoint, auth_headers, updated_data)
    
    log_request_response(put_endpoint, put_response, headers=auth_headers)
    
    # GET
    verify_update_response = SyliusRequest.get(get_endpoint, auth_headers)
    
    log_request_response(get_endpoint, verify_update_response, headers=auth_headers)
    
    # DELETE
    delete_endpoint = EndpointCustomerGroup.code(customer_group_code)
    delete_response = SyliusRequest.delete(delete_endpoint, auth_headers)
    
    log_request_response(delete_endpoint, delete_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)
    
