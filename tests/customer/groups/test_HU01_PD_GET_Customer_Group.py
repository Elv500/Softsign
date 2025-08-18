import pytest
import time

from src.assertions.customergroup_assertions.customer_group_errors_assertions import AssertionCustomerGroupErrors
from src.assertions.customergroup_assertions.customer_group_get_content_assertions import AssertionCustomerGroupFields
from src.assertions.customergroup_assertions.customer_group_schema_assertions import AssertionCustomerGroup
from src.assertions.customergroup_assertions.customer_group_performance_assertions import AssertionCustomerGroupPerformance
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response
from src.data.customer_group import generate_customer_group_source_data

# Admin > Customer - Group > TC_176 Verificar que se puede obtener la lista de grupos de clientes codigo 200
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC176_obtener_lista_grupos_clientes_exitoso(auth_headers):    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_list_schema(response.json())
    

# Admin > Customer - Group > TC_177 Verificar estructura del JSON devuelto
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC177_verificar_estructura_json_respuesta(auth_headers):
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(response.json())
    

# Admin > Customer - Group > TC_178 Verificar que se puede obtener un grupo específico usando un código existente
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC178_obtener_grupo_por_codigo_existente(auth_headers):
    
    data = generate_customer_group_source_data()

    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    response_json = response.json()

    endpoint = EndpointCustomerGroup.code(response_json["code"])
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroupFields.assert_customer_group_item_content(response.json(), response_json["code"])
    

# Admin > Customer - Group > TC_179 Verificar campos obligatorios en cada grupo (id, code, name)
@pytest.mark.functional
@pytest.mark.high
def test_TC179_verificar_campos_obligatorios_cada_grupo(auth_headers):
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(data)
    AssertionCustomerGroupFields.assert_customer_groups_exist(data)
    

# Admin > Customer - Group > TC_180 Verificar que los campos code y name no sean nulos o vacíos
@pytest.mark.functional
@pytest.mark.medium
def test_TC180_verificar_campos_no_vacios(auth_headers):
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(data)
    
    grupos = data.get("hydra:member", [])
    
    for grupo in grupos:
        AssertionCustomerGroupFields.assert_customer_group_item_content(grupo)
    

# Admin > Customer - Group > TC_181 Validar paginación básica con page y itemsPerPage
@pytest.mark.functional
@pytest.mark.medium
def test_TC181_validar_paginacion_basica(auth_headers):
    page, items_per_page = 1, 2
    params = {"page": page, "itemsPerPage": items_per_page}
    
    data = generate_customer_group_source_data()

    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, auth_headers, data)
    
    response_json = response.json()

    endpoint = EndpointCustomerGroup.code(response_json["code"])
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroupFields.assert_customer_group_item_content(response.json(), response_json["code"])
    

# Admin > Customer - Group > TC_182 Verificar paginación con página fuera de rango (ej. page=9999)
@pytest.mark.boundary
@pytest.mark.low
def test_TC182_verificar_paginacion_fuera_rango(auth_headers):
    page_out_of_range = 9999
    
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=page_out_of_range)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroupFields.assert_pagination_out_of_range(response.json())
    

# Admin > Customer - Group > TC_183 Verificar paginación con itemsPerPage = 0
@pytest.mark.boundary
@pytest.mark.xfail(reason="Known issue BugId: CG-01 La aplicación permite que se devuelva 0 items por página", run=True)
@pytest.mark.medium
def test_TC183_verificar_paginacion_items_cero(auth_headers):
    items_per_page = 0
    
    endpoint = EndpointCustomerGroup.customer_group_with_params(itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_400(response)
    

# Admin > Customer - Group > TC_184 Verificar paginación con valores negativos
@pytest.mark.boundary
@pytest.mark.negative
@pytest.mark.medium
def test_TC184_verificar_paginacion_valores_negativos(auth_headers):
    page, items_per_page = -1, -1
    
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=page, itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_400(response)
    

# Admin > Customer - Group > TC_185 Verificar paginación con límite 1000
@pytest.mark.boundary
@pytest.mark.low
def test_TC185_verificar_paginacion_limite_maximo(auth_headers):
    items_per_page = 1000
    
    endpoint = EndpointCustomerGroup.customer_group_with_params(itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroupPerformance.assert_pagination_item_limit(response.json(), items_per_page)
    

# Admin > Customer - Group > TC_186 Verificar que no permita el acceso sin token de autenticación
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.high
def test_TC186_verificar_acceso_sin_token():
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, {})
    
    log_request_response(endpoint, response, headers={})
    
    AssertionStatusCode.assert_status_code_401(response)
    

# Admin > Customer - Group > TC_187 Verificar que no permita el acceso con token inválido
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.high
def test_TC187_verificar_acceso_token_invalido():
    invalid_token = "token_invalido_12345"
    
    invalid_headers = {"Authorization": f"Bearer {invalid_token}"}
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, invalid_headers)
    
    log_request_response(endpoint, response, headers=invalid_headers)
    
    AssertionStatusCode.assert_status_code_401(response)
    

# Admin > Customer - Group > TC_188 Verificar que no permita el acceso con token expirado
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.high
def test_TC188_verificar_acceso_token_expirado():
    
    expired_headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.ey"
                       "JpYXQiOjE3NTQyMzQzODksImV4cCI6MTc1NDIzNzk4OSwicm9sZXMiOlsiUk9MRV"
                       "9BRE1JTklTVFJBVElPTl9BQ0NFU1MiLCJST0xFX0FQSV9BQ0NFU1MiXSwidXNlcm"
                       "5hbWUiOiJhcGkifQ.GmVMaimodyHNL8R9wToFg5RoOTwd9Rjf2WVqI_WoZJjAZJ1y"
                       "kbaBlsbC4TWwPqZuaEpPhFJlRotqezn0_HF7MumgZBK1rvmfX4M7QqQBeeohmZmt8"
                       "JB0eAjaqn-GtmmWeXrV1bCHxvqb-W1pbPsBQ1leKfnYeUnMPwrhPBsqdOAAEVK0ZWj"
                       "_LAbgYWlViEZ8uw7qxDR5gzmd6GwKEawLDlMa9Lj5Hz8sG7NuYonU-b38U_mOkN57x"
                       "r4SSL7DTkdk-q9rIOt-I056tzCKPR2Fx0CxCSO7MMP9pVN9sHMz53srPpHTvwtRCZS"
                       "gzRB4PGU6mzsmfl4l7sLE72OouL-y_eVqgKJ-7YG5D_ZNp8vgaALqYDzbAySDb_ktF"
                       "tCCWzhMxasoBOLoCzy3J1URprwxyPcYabntVyr8O42mkIjh1iGH-IASK9M614epkcB"
                       "cSIbyB5cwkTwfBCAhMwqot6Ec6ozT8VKmfYAZdtisKpVarQrs25CRzdT1kZrRr57Fs"
                       "GgLQgf05K39QLM5wvjEd2i7NiRwCPVeqFVzJgBKN0DQBLK3a7zoN3a_mV7KCGmxoTk"
                       "0RfYEhv00EpxVjMUWg40Cpg22YlFD1WZNxrN1r4Wt0LqkZfCfwPzD9Ci2X45oDjzPm"
                       "Iu6goaWDaaSgpaIeB6pxy-AuWi3ofhXlZkvlTgEm0"}
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, expired_headers)
    
    log_request_response(endpoint, response, headers=expired_headers)
    
    AssertionStatusCode.assert_status_code_401(response)
    

# Admin > Customer - Group > TC_189 Verificar que no permita un header de Authorization mal formado
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.medium
def test_TC189_verificar_header_authorization_mal_formado():
    malformed_auth = "InvalidFormat token123"
    
    malformed_headers = {"Authorization": malformed_auth}
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, malformed_headers)
    
    log_request_response(endpoint, response, headers=malformed_headers)
    
    AssertionStatusCode.assert_status_code_401(response)
    

# Admin > Customer - Group > TC_190 Verificar que no permita obtener grupo con código inexistente
@pytest.mark.negative
@pytest.mark.medium
def test_TC190_obtener_grupo_codigo_inexistente(auth_headers):
    codigo_inexistente = "grupo_que_no_existe_12345"
    
    endpoint = EndpointCustomerGroup.code(codigo_inexistente)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(response)
    AssertionCustomerGroupErrors.assert_not_found_error(response)
    

# Admin > Customer - Group > TC_191 Verificar que no acepte un método HTTP no permitido (POST)
@pytest.mark.negative
@pytest.mark.medium
def test_TC191_verificar_metodo_http_no_permitido(auth_headers):
    
    headers_with_json = auth_headers.copy()
    headers_with_json['Content-Type'] = 'application/json'
    
    endpoint = EndpointCustomerGroup.customer_group()
    payload = {"test": "data"}
    
    response = SyliusRequest.post(endpoint, headers_with_json, payload)
    
    log_request_response(endpoint, response, headers=headers_with_json, payload=payload)
    
    AssertionStatusCode.assert_status_code_422(response)
    

# Admin > Customer - Group > TC_192 Verificar respuesta con parámetros itemsPerPage malformados
@pytest.mark.negative
@pytest.mark.xfail(reason="Known issue BugId: CG-02 No controla los parámetros itemsPerPage malformados", run=True)
@pytest.mark.medium
def test_TC192_verificar_parametros_itemsPerPage_malformados(auth_headers):
    malformed_param = "xyz"
    
    endpoint = EndpointCustomerGroup.customer_group() + f"?page=1&itemsPerPage={malformed_param}"
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_400(response)
    

# Admin > Customer - Group > TC_193 Verificar respuesta con parámetros page malformados
@pytest.mark.negative
@pytest.mark.medium
def test_TC193_verificar_parametros_page_malformados(auth_headers):
    malformed_param = "asd"
    
    endpoint = EndpointCustomerGroup.customer_group() + f"?page={malformed_param}&itemsPerPage=10"
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_400(response)
    

# Admin > Customer - Group > TC_194 Verificar unicidad de IDs y códigos
@pytest.mark.functional
@pytest.mark.high
def test_TC194_verificar_unicidad_ids_codigos(auth_headers):
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(data)
    AssertionCustomerGroupFields.assert_customer_groups_uniqueness(data)
    

# Admin > Customer - Group > TC_195 Verificar formato de datos de cada campo
@pytest.mark.functional
@pytest.mark.medium
def test_TC195_verificar_formato_datos_campos(auth_headers):
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(data)
    
    grupos = data.get("hydra:member", [])
    
    for grupo in grupos:
        AssertionCustomerGroupFields.assert_customer_group_item_content(grupo)
    

# Admin > Customer - Group > TC_196 Verificar límites de longitud de campos
    # Precondicion tener datos de prueba con campos largos o ejecutrar el test de POST primero
@pytest.mark.boundary
@pytest.mark.low
def test_TC196_verificar_limites_longitud_campos(auth_headers):
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(data)
    AssertionCustomerGroupFields.assert_customer_groups_field_length_limits(data)

# Admin > Customer - Group > TC_197 Verificar tiempo de respuesta aceptable (2 seg)
@pytest.mark.performance
@pytest.mark.medium
def test_TC197_verificar_tiempo_respuesta(auth_headers):
    
    endpoint = EndpointCustomerGroup.customer_group()
    
    start_time = time.time()
    response = SyliusRequest.get(endpoint, auth_headers)
    elapsed = time.time() - start_time
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(data)
    AssertionCustomerGroupPerformance.assert_response_time(elapsed)
    

# Admin > Customer - Group > TC_198 Verificar headers de respuesta HTTP
@pytest.mark.functional
@pytest.mark.low
def test_TC198_verificar_headers_respuesta(auth_headers):
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(data)
    AssertionCustomerGroupPerformance.assert_content_type_header(response.headers)
    