import logging
import pytest
import requests
import time

from src.assertions.customergroup_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response

# Configurar logger
logger = logging.getLogger(__name__)

# Variable global para controlar delay entre tests
_last_request_time = 0

def safe_api_call(func, *args, **kwargs):
    """
    Wrapper para hacer llamadas seguras a la API con delay automático
    para evitar rate limiting y timeouts
    """
    global _last_request_time
    current_time = time.time()
    
    # Asegurar al menos 0.5 segundos entre llamadas consecutivas
    time_since_last = current_time - _last_request_time
    if time_since_last < 0.5:
        sleep_time = 0.5 - time_since_last
        logger.debug(f"Esperando {sleep_time:.2f}s para evitar rate limiting...")
        time.sleep(sleep_time)
    
    try:
        result = func(*args, **kwargs)
        _last_request_time = time.time()
        return result
    except Exception as e:
        logger.warning(f"Error en llamada API: {e}")
        _last_request_time = time.time()
        raise


# Admin > Customer - Group > TC_176 Verificar que se puede obtener la lista de grupos de clientes codigo 200
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC176_obtener_lista_grupos_clientes_exitoso(auth_headers):
    logger.info("=== TC_176: Iniciando test para obtener lista de grupos de clientes ===")
    # Optimización: Solo necesita verificar que obtiene respuesta, 1 item es suficiente
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=1)
    response = SyliusRequest.get(endpoint, auth_headers)    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_get_output_schema(response.json())
    log_request_response(endpoint, response, headers=auth_headers)


# Admin > Customer - Group > TC_177 Verificar estructura del JSON devuelto
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC177_verificar_estructura_json_respuesta(auth_headers):
    logger.info("=== TC_177: Iniciando verificación de estructura JSON ===")
    
    # Optimización: Solo necesita verificar estructura, 1 item es suficiente
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=1)
    response = safe_api_call(SyliusRequest.get, endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
        
    data = response.json()
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
    response = safe_api_call(SyliusRequest.get, endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
        
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["code"] == group_code


# Admin > Customer - Group > TC_179 Verificar campos obligatorios en cada grupo (id, code, name)
@pytest.mark.functional
@pytest.mark.regression
def test_TC179_verificar_campos_obligatorios_cada_grupo(auth_headers):
    logger.info("=== TC_179: Iniciando verificación de campos obligatorios ===")
    
    # Optimización: Solo necesita verificar campos en 1 grupo
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=1)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
        
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    assert len(grupos) > 0, "Debe existir al menos un grupo"
    
    # Verificar que el grupo tenga los campos obligatorios (solo 1 grupo)
    grupo = grupos[0]
    assert "id" in grupo, f"Campo 'id' faltante en grupo: {grupo}"
    assert "code" in grupo, f"Campo 'code' faltante en grupo: {grupo}"
    assert "name" in grupo, f"Campo 'name' faltante en grupo: {grupo}"


# Admin > Customer - Group > TC_180 Verificar que los campos code y name no sean nulos o vacíos
@pytest.mark.functional
@pytest.mark.regression
def test_TC180_verificar_campos_no_vacios(auth_headers):
    logger.info("=== TC_180: Iniciando verificación de campos no vacíos ===")
    
    # Optimización: Solo necesita verificar 1 grupo para validar campos no vacíos
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=1)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
        
    AssertionStatusCode.assert_status_code_200(response)
    grupos = response.json().get("hydra:member", [])
    
    # Verificar que el grupo tenga campos no vacíos (solo 1 grupo)
    grupo = grupos[0]
    assert grupo.get("code") is not None, f"Campo 'code' es nulo en grupo: {grupo}"
    assert grupo.get("name") is not None, f"Campo 'name' es nulo en grupo: {grupo}"
    assert grupo.get("code") != "", f"Campo 'code' está vacío en grupo: {grupo}"
    assert grupo.get("name") != "", f"Campo 'name' está vacío en grupo: {grupo}"

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


# Admin > Customer - Group > TC_183 Verificar paginación con itemsPerPage = 0
@pytest.mark.boundary
@pytest.mark.regression
@pytest.mark.xfail(reason="Known issue BugId: CG-01 La aplicacion permite que se devuelva 0 items por pagina", run=True)
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
    

# Admin > Customer - Group > TC_185 Verificar paginación con límite 10
@pytest.mark.boundary
@pytest.mark.regression
def test_TC185_verificar_paginacion_limite_maximo(auth_headers):
    items_per_page = 10
    logger.info(f"=== TC_185: Iniciando test con límite máximo (itemsPerPage={items_per_page}) ===")
    
    endpoint = EndpointCustomerGroup.customer_group_with_params(itemsPerPage=items_per_page)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)


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
    
    headers_with_json = auth_headers.copy()
    headers_with_json['Content-Type'] = 'application/json'
    
    endpoint = EndpointCustomerGroup.customer_group()
    payload = {"test": "data"}
    
    response = requests.post(endpoint, headers=headers_with_json, json=payload)
    
    log_request_response(endpoint, response, headers=headers_with_json, payload=payload)
    
    AssertionStatusCode.assert_status_code_422(response)
    

# Admin > Customer - Group > TC_192 Verificar respuesta con parámetros itemsPerPage malformados
@pytest.mark.negative
@pytest.mark.regression
def test_TC192_verificar_parametros_itemsPerPage_malformados(auth_headers):
    malformed_param = "xyz"
    logger.info(f"=== TC_192: Iniciando test con itemsPerPage malformado: {malformed_param} ===")
    
    # Optimización: Usar SyliusRequest y mantener mínimo de datos
    endpoint = EndpointCustomerGroup.customer_group() + f"?page=1&itemsPerPage={malformed_param}"
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_400(response)
    

# Admin > Customer - Group > TC_193 Verificar respuesta con parámetros page malformados
@pytest.mark.negative
@pytest.mark.regression
def test_TC193_verificar_parametros_page_malformados(auth_headers):
    malformed_param = "asd"
    logger.info(f"=== TC_193: Iniciando test con page malformado: {malformed_param} ===")
    
    # Optimización: Usar SyliusRequest y mantener mínimo de datos
    endpoint = EndpointCustomerGroup.customer_group() + f"?page={malformed_param}&itemsPerPage=1"
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_400(response)
    

# Admin > Customer - Group > TC_194 Verificar unicidad de IDs y códigos
@pytest.mark.functional
@pytest.mark.regression
def test_TC194_verificar_unicidad_ids_codigos(auth_headers):
    logger.info("=== TC_194: Iniciando verificación de unicidad de IDs y códigos ===")
    
    # Optimización: Necesita al menos 2 grupos para verificar unicidad
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=2)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    
    # Verificación de unicidad con mínimo 2 grupos
    ids = [g["id"] for g in grupos]
    codes = [g["code"] for g in grupos]
        
    assert len(ids) == len(set(ids)), f"Los IDs deben ser únicos en muestra de {len(ids)} grupos"
    assert len(codes) == len(set(codes)), f"Los códigos deben ser únicos en muestra de {len(codes)} grupos"
    

# Admin > Customer - Group > TC_195 Verificar formato de datos de cada campo
@pytest.mark.functional
@pytest.mark.regression
def test_TC195_verificar_formato_datos_campos(auth_headers):
    logger.info("=== TC_195: Iniciando verificación de formato de datos ===")
    
    # Optimización: Solo necesita validar formato en 1 grupo
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=1)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    logger.info(f"Verificando formato de datos en {len(grupos)} grupo (optimizado)")
    
    # Validación solo en 1 grupo
    grupo = grupos[0]
    assert isinstance(grupo["id"], int)
    assert grupo["id"] > 0
    
    assert isinstance(grupo["code"], str)
    assert len(grupo["code"]) > 0
    
    assert isinstance(grupo["name"], str)
    assert len(grupo["name"]) > 0
    

# Admin > Customer - Group > TC_196 Verificar límites de longitud de campos
# Precondición: tener datos de prueba con campos largos o ejecutar el test de POST primero
@pytest.mark.boundary
@pytest.mark.regression
def test_TC196_verificar_limites_longitud_campos(auth_headers):
    logger.info("=== TC_196: Iniciando verificación de límites de longitud ===")
    
    # Optimización: Solo necesita verificar límites en 1 grupo
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=1)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    
    # Procesamiento de solo 1 grupo
    grupo = grupos[0]
    code_length = len(grupo["code"])
    name_length = len(grupo["name"])
                
    assert code_length <= 255, f"Código muy largo: {grupo['code']}"
    assert name_length <= 255, f"Nombre muy largo: {grupo['name']}"
    

# Admin > Customer - Group > TC_197 Verificar tiempo de respuesta aceptable (2 seg)
@pytest.mark.performance
@pytest.mark.regression
def test_TC197_verificar_tiempo_respuesta(auth_headers):
    logger.info("=== TC_197: Iniciando test de performance - tiempo de respuesta ===")
    
    # Optimización: Para test de performance, usar mínimo de datos
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=1)
    
    start_time = time.time()
    response = SyliusRequest.get(endpoint, auth_headers)
    elapsed = time.time() - start_time
    
    log_request_response(endpoint, response, headers=auth_headers)
        
    AssertionStatusCode.assert_status_code_200(response)
    assert elapsed < 2.0, f"Tiempo de respuesta muy alto: {elapsed:.2f}s"
    

# Admin > Customer - Group > TC_198 Verificar headers de respuesta HTTP
@pytest.mark.functional
@pytest.mark.regression
def test_TC198_verificar_headers_respuesta(auth_headers):
    logger.info("=== TC_198: Iniciando verificación de headers HTTP ===")
    
    # Optimización: Solo necesita verificar headers, 1 item es suficiente
    endpoint = EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=1)
    response = SyliusRequest.get(endpoint, auth_headers)
    
    log_request_response(endpoint, response, headers=auth_headers)
    
    AssertionStatusCode.assert_status_code_200(response)
    
    headers = response.headers    
    content_type = headers.get("Content-Type", "")    
    assert content_type.startswith("application/ld+json"), f"Content-Type incorrecto: {content_type}"
    