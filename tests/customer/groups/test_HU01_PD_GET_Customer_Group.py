import jsonschema
import pytest
import time

from src.assertions.customergroup_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest


# Admin > Customer - Group > TC_176 Verificar que se puede obtener la lista de grupos de clientes codigo 200
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC176_obtener_lista_grupos_clientes_exitoso(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_get_output_schema(response.json())


# Admin > Customer - Group > TC_177 Verificar estructura del JSON devuelto
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_TC177_verificar_estructura_json_respuesta(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    data = response.json()
    
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
    response = SyliusRequest.get(EndpointCustomerGroup.code(group_code), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["code"] == group_code


# Admin > Customer - Group > TC_179 Verificar campos obligatorios en cada grupo (id, code, name)
@pytest.mark.functional
@pytest.mark.regression
def test_TC179_verificar_campos_obligatorios_cada_grupo(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    assert len(grupos) > 0, "Debe existir al menos un grupo"
    
    for grupo in grupos:
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
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    
    for grupo in response.json().get("hydra:member", []):
        assert grupo["code"].strip() != "", f"El código no debe estar vacío para grupo {grupo['id']}"
        assert grupo["name"].strip() != "", f"El nombre no debe estar vacío para grupo {grupo['id']}"


# Admin > Customer - Group > TC_181 Validar paginación básica con page y itemsPerPage
@pytest.mark.functional
@pytest.mark.regression
def test_TC181_validar_paginacion_basica(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group_with_params(page=1, itemsPerPage=2), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    assert isinstance(data.get("hydra:member", []), list)
    assert len(data["hydra:member"]) <= 2


# Admin > Customer - Group > TC_182 Verificar paginación con página fuera de rango (ej. page=9999)
@pytest.mark.boundary
@pytest.mark.regression
def test_TC182_verificar_paginacion_fuera_rango(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group_with_params(page=9999), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    assert isinstance(data.get("hydra:member", []), list)


# Admin > Customer - Group > TC_183 Verificar paginación con itemsPerPage = 0
@pytest.mark.boundary
@pytest.mark.regression
def test_TC183_verificar_paginacion_items_cero(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group_with_params(itemsPerPage=0), auth_headers)
    AssertionStatusCode.assert_status_code_400(response)


# Admin > Customer - Group > TC_184 Verificar paginación con valores negativos
@pytest.mark.boundary
@pytest.mark.negative
@pytest.mark.regression
def test_TC184_verificar_paginacion_valores_negativos(auth_headers):
    """Verificar comportamiento con valores negativos en paginación"""
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group_with_params(page=-1, itemsPerPage=-1), auth_headers)
    AssertionStatusCode.assert_status_code_400(response)


# Admin > Customer - Group > TC_185 Verificar paginación con límite 1000
@pytest.mark.boundary
@pytest.mark.regression
def test_TC185_verificar_paginacion_limite_maximo(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group_with_params(itemsPerPage=1000), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    
    data = response.json()
    assert len(data["hydra:member"]) <= 1000


# Admin > Customer - Group > TC_186 Verificar que no permita el acceso sin token de autenticación
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.regression
def test_TC186_verificar_acceso_sin_token():
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), {})
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_187 Verificar que no permita el acceso con token inválido
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.regression
def test_TC187_verificar_acceso_token_invalido():
    invalid_headers = {"Authorization": "Bearer token_invalido_12345"}
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), invalid_headers)
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_188 Verificar que no permita el acceso con token expirado
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.regression
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
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), expired_headers)
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_189 Verificar que no permita un header de Authorization mal formado
@pytest.mark.security
@pytest.mark.negative
@pytest.mark.regression
def test_TC189_verificar_header_authorization_mal_formado():
    malformed_headers = {"Authorization": "InvalidFormat token123"}
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), malformed_headers)
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > TC_190 Verificar que no permita obtener grupo con código inexistente
@pytest.mark.negative
@pytest.mark.regression
def test_TC190_obtener_grupo_codigo_inexistente(auth_headers):
    codigo_inexistente = "grupo_que_no_existe_12345"
    response = SyliusRequest.get(EndpointCustomerGroup.code(codigo_inexistente), auth_headers)
    AssertionStatusCode.assert_status_code_404(response)


# Admin > Customer - Group > TC_191 Verificar que no acepte un método HTTP no permitido (POST)
@pytest.mark.negative
@pytest.mark.regression
def test_TC191_verificar_metodo_http_no_permitido(auth_headers):
    import requests
    headers_with_json = auth_headers.copy()
    headers_with_json['Content-Type'] = 'application/json'
    
    response = requests.post(
        EndpointCustomerGroup.customer_group(),
        headers=headers_with_json,
        json={"test": "data"}
    )
    AssertionStatusCode.assert_status_code_415(response)


# Admin > Customer - Group > TC_192 Verificar respuesta con parámetros itemsPerPage malformados
@pytest.mark.negative
@pytest.mark.regression
def test_TC192_verificar_parametros_itemsPerPage_malformados(auth_headers):
    import requests
    url = EndpointCustomerGroup.customer_group() + "?page=1&itemsPerPage=xyz"
    response = requests.get(url, headers=auth_headers)
    AssertionStatusCode.assert_status_code_400(response)


# Admin > Customer - Group > TC_193 Verificar respuesta con parámetros page malformados
@pytest.mark.negative
@pytest.mark.regression
def test_TC193_verificar_parametros_page_malformados(auth_headers):
    import requests
    url = EndpointCustomerGroup.customer_group() + "?page=asd&itemsPerPage=10"
    response = requests.get(url, headers=auth_headers)
    AssertionStatusCode.assert_status_code_400(response)


# Admin > Customer - Group > TC_194 Verificar unicidad de IDs y códigos
@pytest.mark.functional
@pytest.mark.regression
def test_TC194_verificar_unicidad_ids_codigos(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    
    grupos = response.json().get("hydra:member", [])
    ids = [g["id"] for g in grupos]
    codes = [g["code"] for g in grupos]
    
    assert len(ids) == len(set(ids)), "Los IDs deben ser únicos"
    assert len(codes) == len(set(codes)), "Los códigos deben ser únicos"


# Admin > Customer - Group > TC_195 Verificar formato de datos de cada campo
@pytest.mark.functional
@pytest.mark.regression
def test_TC195_verificar_formato_datos_campos(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    
    for grupo in response.json().get("hydra:member", []):
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
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    
    for grupo in response.json().get("hydra:member", []):
        assert len(grupo["code"]) <= 255, f"Código muy largo: {grupo['code']}"
        assert len(grupo["name"]) <= 255, f"Nombre muy largo: {grupo['name']}"


# Admin > Customer - Group > TC_197 Verificar tiempo de respuesta aceptable (2 seg)
@pytest.mark.performance
@pytest.mark.regression
def test_TC197_verificar_tiempo_respuesta(auth_headers):
    start_time = time.time()
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    elapsed = time.time() - start_time
    
    AssertionStatusCode.assert_status_code_200(response)
    assert elapsed < 2.0, f"Tiempo de respuesta muy alto: {elapsed:.2f}s"


# Admin > Customer - Group > TC_198 Verificar headers de respuesta HTTP
@pytest.mark.functional
@pytest.mark.regression
def test_TC198_verificar_headers_respuesta(auth_headers):
    response = SyliusRequest.get(EndpointCustomerGroup.customer_group(), auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    
    headers = response.headers
    content_type = headers.get("Content-Type", "")
    assert content_type.startswith("application/ld+json"), f"Content-Type incorrecto: {content_type}"
