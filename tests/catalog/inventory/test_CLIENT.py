# from src.routes.client import SyliusClient

# from src.routes.endpoint_inventory import EndpointInventory
# from src.routes.request import SyliusRequest
# from utils.logger_helpers import log_request_response

# def test_Request(auth_headers):
#     params = {"itemsPerPage": 2}
#     url = EndpointInventory.inventory_with_params(**params)
#     response = SyliusRequest.get(url, auth_headers)
#     assert response.status_code == 200
#     log_request_response(url, response, auth_headers)

# def test_Cient(auth_headers):
#     params = {"itemsPerPage": 2}
#     url = EndpointInventory.inventory_with_params(**params)
#     response = SyliusClient.get(url, auth_headers)

#     assert response.status == 200
#     log_request_response(url, response, auth_headers)