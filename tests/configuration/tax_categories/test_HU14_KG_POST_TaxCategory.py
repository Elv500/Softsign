import pytest

from src.assertions.TaxCategory_assertions.taxCategory_schema_assertions import AssertionTaxCategory
from src.assertions.TaxCategory_assertions.tax_category_post_content_assertions import AssertionTaxCategoryCreate
from src.assertions.TaxCategory_assertions.tax_category_errors_assertions import AssertionTaxCategoryErrors
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_tax_category import EndpointTaxCategory
from src.routes.request import SyliusRequest
from src.data.taxCategory import generate_tax_category_data
from utils.logger_helpers import log_request_response
from src.resources.call_request.taxCategory_call import TaxCategoryCall

"""
TC60 - Crear categoría de impuesto exitosamente: La API debe permitir crear una categoría de impuesto
cuando se envían datos válidos. Esperado: HTTP 201 Created y estructura JSON correcta.
"""
@pytest.mark.high
@pytest.mark.smoke
@pytest.mark.functional
def test_TC60_Crear_categoria_impuesto_exitosamente(setup_add_tax_category):
    headers, created_tax_categories = setup_add_tax_category
    payload = generate_tax_category_data()
    url = EndpointTaxCategory.tax_category()
    response = SyliusRequest.post(url, headers, payload)
    AssertionTaxCategory.assert_tax_category_input_schema(payload)
    AssertionTaxCategoryCreate.assert_tax_category_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionTaxCategory.assert_tax_category_output_schema(response_json)
    AssertionTaxCategoryCreate.assert_tax_category_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_tax_categories.append(response_json)


"""
TC62 - Negativo: El sistema no debe permitir crear dos categorías con el mismo código.
Esperado: status 422 y detalle del error en 'violations'.
"""
@pytest.mark.high
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC62_error_por_codigo_duplicado(setup_add_tax_category):
    headers, created_tax_categories = setup_add_tax_category
    payload = generate_tax_category_data()
    AssertionTaxCategory.assert_tax_category_input_schema(payload)
    AssertionTaxCategoryCreate.assert_tax_category_payload(payload)
    response_1 = TaxCategoryCall.create(headers, payload)
    log_request_response(EndpointTaxCategory.tax_category(), response_1, headers, payload)
    AssertionStatusCode.assert_status_code_201(response_1)
    AssertionTaxCategory.assert_tax_category_output_schema(response_1.json())
    AssertionTaxCategoryCreate.assert_tax_category_response(payload, response_1.json())
    created_tax_categories.append(response_1.json())
    response_2 = TaxCategoryCall.create(headers, payload)
    log_request_response(EndpointTaxCategory.tax_category(), response_2, headers, payload)
    AssertionStatusCode.assert_status_code_422(response_2)
    AssertionTaxCategoryErrors.assert_duplicate_code_error(response_2.json())


"""
TC150 - Negativo: No debe permitir crear una categoría con token inválido (401 Unauthorized).
"""
@pytest.mark.high
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC150_creacion_con_token_invalido(setup_add_tax_category):
    payload = generate_tax_category_data()
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    AssertionTaxCategory.assert_tax_category_input_schema(payload)
    AssertionTaxCategoryCreate.assert_tax_category_payload(payload)
    response = TaxCategoryCall.create(invalid_headers, payload)
    log_request_response(EndpointTaxCategory.tax_category(), response, invalid_headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxCategoryErrors.assert_invalid_token_error(response.json())


"""
TC68 - Negativo: El sistema debe rechazar la creación de categoría si no se proporciona token de autenticación (HTTP 401).
"""
@pytest.mark.high
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC68_creacion_sin_autenticacion(setup_add_tax_category):
    data = generate_tax_category_data()
    empty_headers = {}
    response = TaxCategoryCall.create(empty_headers, data)
    log_request_response(EndpointTaxCategory.tax_category(), response, empty_headers, data)
    AssertionStatusCode.assert_status_code_401(response)


"""
TC63 - Validación de encabezados: La respuesta al crear una categoría de impuesto debe incluir 
el encabezado 'Content-Type' y su valor debe comenzar con 'application/ld+json'.
"""
@pytest.mark.medium
@pytest.mark.functional
@pytest.mark.smoke
def test_TC63_verificar_encabezados_respuesta(setup_add_tax_category):
    headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_data()
    response = TaxCategoryCall.create(headers, data)
    AssertionStatusCode.assert_status_code_201(response)
    log_request_response(EndpointTaxCategory.tax_category(), response, headers, data)
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"].startswith("application/ld+json")
    created_tax_categories.append(response.json())



""""
TC-64: Este caso de prueba valida que los campos principales devueltos por la API al crear una categoría de impuesto (code, name, description)
tengan el tipo de dato correcto. Se espera que todos los campos sean cadenas de texto (string) 
según la especificación del esquema de respuesta.
"""
@pytest.mark.medium
@pytest.mark.functional
@pytest.mark.smoke
def test_TC64_verificar_formato_y_tipos_datos_en_respuesta(setup_add_tax_category):
    headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_data()
    response = TaxCategoryCall.create(headers, data)
    AssertionStatusCode.assert_status_code_201(response)
    log_request_response(EndpointTaxCategory.tax_category(),response, headers,data)
    res_json = response.json()
    assert isinstance(res_json["code"], str)
    assert isinstance(res_json["name"], str)
    assert isinstance(res_json["description"], str)
    created_tax_categories.append(res_json)



"""
TC65 - Negativo: No debe permitirse crear una categoría de impuesto con un código que exceda el límite máximo de longitud.
"""
@pytest.mark.medium
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.domain
def test_TC65_validar_limite_longitud_code(auth_headers):
    data = generate_tax_category_data()
    data["code"] = "A" * 256
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(EndpointTaxCategory.tax_category(), response, auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)



"""
TC66 - Negativo: Validar que el sistema rechaza la creación de una categoría de impuesto
cuando el campo 'code' contiene caracteres especiales no permitidos como '@', '#', '%'.
"""
@pytest.mark.medium
@pytest.mark.functional
@pytest.mark.smoke
def test_TC66_validar_caracteres_especiales_en_code(auth_headers):
    data = generate_tax_category_data()
    data["code"] = "ABC@#%"
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(EndpointTaxCategory.tax_category(), response, auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)


"""
TC67 - Validar que el sistema permite la creación de una categoría de impuesto
con el campo 'description' vacío.
"""
@pytest.mark.medium
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.domain
def test_TC67_description_vacio(auth_headers):
    data = generate_tax_category_data()
    data["description"] = ""
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(url=EndpointTaxCategory.tax_category(), response=response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_201(response)


"""
TC221 - Negativo: Validar que el sistema rechaza la creación de una categoría de impuesto
si se omite el campo obligatorio 'name'.
"""
@pytest.mark.high
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC221_creacion_sin_nombre_categoria(auth_headers):
    data = generate_tax_category_data()
    data.pop("name", None)
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(url=EndpointTaxCategory.tax_category(), response=response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxCategoryErrors.assert_missing_field_error(response_json, "name")

"""
No debe permitir crear una categoría con nombre menor a 2 caracteres (Sylius debe responder 422).
"""
@pytest.mark.medium
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.domain
@pytest.mark.parametrize("invalid_name", [
    "",    # vacío
    "A",   # un solo carácter
])
def test_TC255_tax_category_nombre_minimo_length(setup_add_tax_category, invalid_name):

    auth_headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_data()
    data["name"] = invalid_name
    url = EndpointTaxCategory.tax_category()
    response = TaxCategoryCall.create(auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)
    log_request_response(EndpointTaxCategory.tax_category(), response, auth_headers, data)


"""
TC-220 No debe permitir crear una categoría de impuesto con un nombre mayor a 255 caracteres.
Sylius debe responder con un código de estado HTTP 422.
"""
@pytest.mark.medium
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.negative
def test_TC220_tax_category_nombre_exedente_maximo_length(setup_add_tax_category):
    auth_headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_data()
    data["name"] = "A" * 256  # nombre con 256 caracteres (excede el máximo permitido)
    url = EndpointTaxCategory.tax_category()
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(url, response, auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxCategoryErrors.assert_max_length_error(response_json, "name")


"""
No debe permitir crear una categoría de impuesto si el nombre solo contiene
espacios en blanco, saltos de línea u otros caracteres invisibles. Sylius debe responder con 422.
"""
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
@pytest.mark.negative
@pytest.mark.domain
@pytest.mark.xfail(reason="known issue La app permite espacios vacios BUG", run=True)
@pytest.mark.parametrize("invalid_name", [
    "   ",
    "\n",
    "\n\n",
    " \n ",
    "\t",
    " \t \n "
])
def test_TC221_tax_category_nombre_espacio_en_blanco(setup_add_tax_category, invalid_name):

    auth_headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_data()
    data["name"] = invalid_name
    url = EndpointTaxCategory.tax_category()
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(EndpointTaxCategory.tax_category(), response, auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxCategoryErrors.assert_missing_field_error(response_json, "name")




#TC 418 Admin > Configuration > Tax category - Crear Tax Category sin code
@pytest.mark.high
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.negative
def test_TC418_crear_tax_category_sin_code(auth_headers):
    data = generate_tax_category_data()
    data.pop("code", None)
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(url=EndpointTaxCategory.tax_category(), response=response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxCategoryErrors.assert_missing_field_error(response_json, "code")