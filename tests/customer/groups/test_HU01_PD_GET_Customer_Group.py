import logging
import pytest
import time

from src.assertions.customergroup_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response

# Configurar logger
logger = logging.getLogger(__name__)


# Admin > Customer - Group > TC_176 Verificar que se puede obtener la lista de grupos de clientes codigo 200
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC176_obtener_lista_grupos_clientes_exitoso(auth_headers):
    logger.info("=== TC_176: Iniciando test para obtener lista de grupos de clientes ===")
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_get_output_schema(response.json())
    

# Admin > Customer - Group > TC_177 Verificar estructura del JSON devuelto
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC177_verificar_estructura_json_respuesta(auth_headers):
    logger.info("=== TC_177: Iniciando verificación de estructura JSON ===")
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    data = response.json()
    logger.info(f"Estructura JSON - Keys: {list(data.keys())}")
    logger.info(f"Cantidad de elementos en hydra:member: {len(data.get('hydra:member', []))}")
    logger.info(f"Total items: {data.get('hydra:totalItems', 'N/A')}")
    
    AssertionStatusCode.assert_status_code_200(response)
    
    assert "hydra:member" in data
    assert "hydra:totalItems" in data
    assert isinstance(data["hydra:member"], list)
    assert isinstance(data["hydra:totalItems"], int)
    

# Admin > Customer - Group > TC_178 Verificar que se puede obtener un grupo específico usando un código existente
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC178_obtener_grupo_por_codigo_existente(auth_headers):
    group_code = "retail"
    logger.info(f"=== TC_178: Iniciando test para obtener grupo específico: {group_code} ===")
    
    endpoint = EndpointCustomerGroup.code(group_code)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["code"] == group_code
    

# Admin > Customer - Group > TC_179 Verificar campos obligatorios en cada grupo (id, code, name)
@pytest.mark.functional
@pytest.mark.regression
def test_TC179_verificar_campos_obligatorios_cada_grupo(auth_headers):
    logger.info("=== TC_179: Iniciando verificación de campos obligatorios ===")
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    logger.info(f"Cantidad de grupos a verificar: {len(grupos)}")
    assert len(grupos) > 0, "Debe existir al menos un grupo"
    
    for i, grupo in enumerate(grupos):
        logger.debug(f"Verificando grupo {i+1}: ID={grupo.get('id')}, Code={grupo.get('code')}")
        assert "id" in grupo
        assert "code" in grupo
        assert "name" in grupo
        assert grupo["id"] is not None
        assert grupo["code"] is not None
        assert grupo["name"] is not None
    

# Admin > Customer - Group > TC_180 Verificar que los campos code y name no sean nulos o vacíos
@pytest.mark.functional
@pytest.mark.regression
def test_TC180_verificar_campos_no_vacios(auth_headers):
    logger.info("=== TC_180: Iniciando verificación de campos no vacíos ===")
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    logger.info(f"Verificando {len(grupos)} grupos para campos no vacíos")
    
    for i, grupo in enumerate(grupos):
        logger.debug(f"Grupo {i+1}: code='{grupo['code']}', name='{grupo['name']}'")
        assert grupo["code"].strip() != "", f"El código no debe estar vacío para grupo {grupo['id']}"
        assert grupo["name"].strip() != "", f"El nombre no debe estar vacío para grupo {grupo['id']}"
    

# Admin > Customer - Group > TC_181 Validar paginación básica con page y itemsPerPage
@pytest.mark.functional
@pytest.mark.regression
def test_TC181_validar_paginacion_basica(auth_headers):
    page, items_per_page = 1, 2
    logger.info(f"=== TC_181: Iniciando test de paginación básica (page={page}, itemsPerPage={items_per_page}) ===")
    
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=page, itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    member_count = len(data["hydra:member"])
    logger.info(f"Elementos recibidos: {member_count}, Límite solicitado: {items_per_page}")
    logger.info(f"Total items disponibles: {data.get('hydra:totalItems', 'N/A')}")
    
    assert isinstance(data.get("hydra:member", []), list)
    assert member_count <= items_per_page
    

# Admin > Customer - Group > TC_182 Verificar paginación con página fuera de rango (ej. page=9999)
@pytest.mark.boundary
@pytest.mark.regression
def test_TC182_verificar_paginacion_fuera_rango(auth_headers):
    page_out_of_range = 9999
    logger.info(f"=== TC_182: Iniciando test de paginación fuera de rango (page={page_out_of_range}) ===")
    
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=page_out_of_range)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    member_count = len(data.get("hydra:member", []))
    logger.info(f"Elementos recibidos en página fuera de rango: {member_count}")
    logger.info(f"Total items disponibles: {data.get('hydra:totalItems', 'N/A')}")
    
    assert isinstance(data.get("hydra:member", []), list)
    

# Admin > Customer - Group > TC_183 Verificar paginación con itemsPerPage = 0
@pytest.mark.boundary
@pytest.mark.regression
def test_TC183_verificar_paginacion_items_cero(auth_headers):
    items_per_page = 0
    logger.info(f"=== TC_183: Iniciando test de paginación con itemsPerPage={items_per_page} ===")
    
    endpoint = EndpointCustomerGroup.customer_group_with_params(itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_400(response)
    

# Admin > Customer - Group > TC_184 Verificar paginación con valores negativos
@pytest.mark.boundary
@pytest.mark.negative
@pytest.mark.regression
def test_TC184_verificar_paginacion_valores_negativos(auth_headers):
    page, items_per_page = -1, -1
    logger.info(f"=== TC_184: Iniciando test con valores negativos (page={page}, itemsPerPage={items_per_page}) ===")
    
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=page, itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_400(response)
    

# Admin > Customer - Group > TC_185 Verificar paginación con límite 1000
@pytest.mark.boundary
@pytest.mark.regression
def test_TC185_verificar_paginacion_limite_maximo(auth_headers):
    items_per_page = 1000
    logger.info(f"=== TC_185: Iniciando test con límite máximo (itemsPerPage={items_per_page}) ===")
    
    endpoint = EndpointCustomerGroup.customer_group_with_params(itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    member_count = len(data["hydra:member"])
    logger.info(f"Elementos recibidos: {member_count}, Límite solicitado: {items_per_page}")
    logger.info(f"Total items disponibles: {data.get('hydra:totalItems', 'N/A')}")
    
    assert member_count <= items_per_page
    

# Admin > Customer - Group > TC_186 Verificar que no permita el acceso sin token de autenticación
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.regression
def test_TC186_verificar_acceso_sin_token():
    logger.info("=== TC_186: Iniciando test de seguridad - acceso sin token ===")
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, {})
    
    log_request_response(endpoint, response, headers={})
    
    AssertionStatusCode.assert_status_code_401(response)
    

# Admin > Customer - Group > TC_187 Verificar que no permita el acceso con token inválido
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.regression
def test_TC187_verificar_acceso_token_invalido():
    invalid_token = "token_invalido_12345"
    logger.info("=== TC_187: Iniciando test de seguridad - token inválido ===")
    logger.info(f"Token usado: {invalid_token[:20]}...")
    
    invalid_headers = {"Authorization": f"Bearer {invalid_token}"}
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, invalid_headers)
    
    log_request_response(endpoint, response, headers=invalid_headers)
    
    AssertionStatusCode.assert_status_code_401(response)
    

# Admin > Customer - Group > TC_188 Verificar que no permita el acceso con token expirado
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.regression
def test_TC188_verificar_acceso_token_expirado():
    logger.info("=== TC_188: Iniciando test de seguridad - token expirado ===")
    logger.info("Usando token JWT con fecha de expiración pasada")
    
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
@pytest.mark.regression
def test_TC189_verificar_header_authorization_mal_formado():
    malformed_auth = "InvalidFormat token123"
    logger.info("=== TC_189: Iniciando test de seguridad - header Authorization malformado ===")
    logger.info(f"Header malformado usado: {malformed_auth}")
    
    malformed_headers = {"Authorization": malformed_auth}
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, malformed_headers)
    
    log_request_response(endpoint, response, headers=malformed_headers)
    
    AssertionStatusCode.assert_status_code_401(response)
    

# Admin > Customer - Group > TC_190 Verificar que no permita obtener grupo con código inexistente
@pytest.mark.negative
@pytest.mark.regression
def test_TC190_obtener_grupo_codigo_inexistente(auth_headers):
    codigo_inexistente = "grupo_que_no_existe_12345"
    logger.info(f"=== TC_190: Iniciando test con código inexistente: {codigo_inexistente} ===")
    
    endpoint = EndpointCustomerGroup.code(codigo_inexistente)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_404(response)
    

# Admin > Customer - Group > TC_191 Verificar que no acepte un método HTTP no permitido (POST)
@pytest.mark.negative
@pytest.mark.regression
def test_TC191_verificar_metodo_http_no_permitido(auth_headers):
    logger.info("=== TC_191: Iniciando test de método HTTP no permitido (POST) ===")
    logger.info("Enviando POST request a endpoint GET")
    
    import requests
    headers_with_json = auth_headers.copy()
    headers_with_json['Content-Type'] = 'application/json'
    
    endpoint = EndpointCustomerGroup.customer_group()
    payload = {"test": "data"}
    
    logger.info(f"Headers enviados: Content-Type: application/json + Authorization")
    logger.info(f"Body JSON: {payload}")
    
    response = requests.post(endpoint, headers=headers_with_json, json=payload)
    
    log_request_response(endpoint, response, headers=headers_with_json, payload=payload)
    
    AssertionStatusCode.assert_status_code_415(response)
    

# Admin > Customer - Group > TC_192 Verificar respuesta con parámetros itemsPerPage malformados
@pytest.mark.negative
@pytest.mark.regression
def test_TC192_verificar_parametros_itemsPerPage_malformados(auth_headers):
    malformed_param = "xyz"
    logger.info(f"=== TC_192: Iniciando test con itemsPerPage malformado: {malformed_param} ===")
    
    import requests
    endpoint = EndpointCustomerGroup.customer_group() + f"?page=1&itemsPerPage={malformed_param}"
    response = requests.get(endpoint, headers=auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_400(response)
    

# Admin > Customer - Group > TC_193 Verificar respuesta con parámetros page malformados
@pytest.mark.negative
@pytest.mark.regression
def test_TC193_verificar_parametros_page_malformados(auth_headers):
    malformed_param = "asd"
    logger.info(f"=== TC_193: Iniciando test con page malformado: {malformed_param} ===")
    
    import requests
    endpoint = EndpointCustomerGroup.customer_group() + f"?page={malformed_param}&itemsPerPage=10"
    response = requests.get(endpoint, headers=auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_400(response)
    

# Admin > Customer - Group > TC_194 Verificar unicidad de IDs y códigos
@pytest.mark.functional
@pytest.mark.regression
def test_TC194_verificar_unicidad_ids_codigos(auth_headers):
    logger.info("=== TC_194: Iniciando verificación de unicidad de IDs y códigos ===")
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    logger.info(f"Verificando unicidad en {len(grupos)} grupos")
    
    ids = [g["id"] for g in grupos]
    codes = [g["code"] for g in grupos]
    
    logger.info(f"IDs encontrados: {len(ids)}, IDs únicos: {len(set(ids))}")
    logger.info(f"Códigos encontrados: {len(codes)}, Códigos únicos: {len(set(codes))}")
    
    assert len(ids) == len(set(ids)), "Los IDs deben ser únicos"
    assert len(codes) == len(set(codes)), "Los códigos deben ser únicos"
    

# Admin > Customer - Group > TC_195 Verificar formato de datos de cada campo
@pytest.mark.functional
@pytest.mark.regression
def test_TC195_verificar_formato_datos_campos(auth_headers):
    logger.info("=== TC_195: Iniciando verificación de formato de datos ===")
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    logger.info(f"Verificando formato de datos en {len(grupos)} grupos")
    
    for i, grupo in enumerate(grupos):
        logger.debug(f"Grupo {i+1}: ID={grupo['id']} (tipo: {type(grupo['id'])})")
        logger.debug(f"Grupo {i+1}: Code='{grupo['code']}' (tipo: {type(grupo['code'])}, longitud: {len(grupo['code'])})")
        logger.debug(f"Grupo {i+1}: Name='{grupo['name']}' (tipo: {type(grupo['name'])}, longitud: {len(grupo['name'])})")
        
        assert isinstance(grupo["id"], int)
        assert grupo["id"] > 0
        
        assert isinstance(grupo["code"], str)
        assert len(grupo["code"]) > 0
        
        assert isinstance(grupo["name"], str)
        assert len(grupo["name"]) > 0
    

# Admin > Customer - Group > TC_196 Verificar límites de longitud de campos
    # Precondicion tener datos de prueba con campos largos o ejecutrar el test de POST primero
@pytest.mark.boundary
@pytest.mark.regression
def test_TC196_verificar_limites_longitud_campos(auth_headers):
    logger.info("=== TC_196: Iniciando verificación de límites de longitud ===")
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    logger.info(f"Verificando límites de longitud en {len(grupos)} grupos")
    
    max_code_length = 0
    max_name_length = 0
    
    for i, grupo in enumerate(grupos):
        code_length = len(grupo["code"])
        name_length = len(grupo["name"])
        
        if code_length > max_code_length:
            max_code_length = code_length
        if name_length > max_name_length:
            max_name_length = name_length
            
        logger.debug(f"Grupo {i+1}: Code length={code_length}, Name length={name_length}")
        
        assert code_length <= 255, f"Código muy largo: {grupo['code']}"
        assert name_length <= 255, f"Nombre muy largo: {grupo['name']}"
    
    logger.info(f"Longitud máxima de código encontrada: {max_code_length}")
    logger.info(f"Longitud máxima de nombre encontrada: {max_name_length}")

# Admin > Customer - Group > TC_197 Verificar tiempo de respuesta aceptable (2 seg)
@pytest.mark.performance
@pytest.mark.regression
def test_TC197_verificar_tiempo_respuesta(auth_headers):
    logger.info("=== TC_197: Iniciando test de performance - tiempo de respuesta ===")
    logger.info("Límite de tiempo esperado: 2.0 segundos")
    
    endpoint = EndpointCustomerGroup.customer_group()
    
    start_time = time.time()
    response = SyliusRequest.get(endpoint, auth_headers)
    elapsed = time.time() - start_time
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    logger.info(f"Tiempo de respuesta: {elapsed:.3f} segundos")
    logger.info(f"Tamaño de respuesta: {len(response.content)} bytes")
    
    AssertionStatusCode.assert_status_code_200(response)
    assert elapsed < 2.0, f"Tiempo de respuesta muy alto: {elapsed:.2f}s"
    

# Admin > Customer - Group > TC_198 Verificar headers de respuesta HTTP
@pytest.mark.functional
@pytest.mark.regression
def test_TC198_verificar_headers_respuesta(auth_headers):
    logger.info("=== TC_198: Iniciando verificación de headers HTTP ===")
    
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    headers = response.headers
    logger.info(f"Headers de respuesta recibidos: {dict(headers)}")
    
    content_type = headers.get("Content-Type", "")
    logger.info(f"Content-Type: {content_type}")
    
    assert content_type.startswith("application/ld+json"), f"Content-Type incorrecto: {content_type}"
    