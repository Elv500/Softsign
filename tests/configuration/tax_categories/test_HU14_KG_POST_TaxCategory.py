import pytest

from src.routes.request import SyliusRequest
from src.assertions.taxCategory_assertions import AssertionTaxCategory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.data.taxCategory import generate_tax_category_data
from src.routes.endpoint_tax_category import EndpointTaxCategory
from src.resources.call_request.taxCategory_call import TaxCategoryCall
from utils.logger_helpers import log_request_response


"""
TC60 - Crear categoría de impuesto exitosamente: La API debe permitir crear una categoría de impuesto
cuando se envían datos válidos. Esperado: HTTP 201 Created y estructura JSON correcta.
"""
@pytest.mark.smoke
@pytest.mark.functional
def test_TC60_Crear_categoría_de_impuesto_exitosamente(setup_add_tax_category):
    headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_data()
    url = EndpointTaxCategory.tax_category()
    response = SyliusRequest().post(EndpointTaxCategory.tax_category(), headers, data)
    log_request_response(url, response, headers, data)
    AssertionTaxCategory.assert_tax_category_input_schema(data)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxCategory.assert_tax_category_output_schema(response.json())
    created_category = response.json()
    created_tax_categories.append(created_category)


"""
TC62 - Negativo: El sistema no debe permitir crear dos categorías con el mismo código.
Esperado: status 422 y detalle del error en 'violations'.
"""
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC62_error_por_codigo_duplicado(setup_add_tax_category):
    headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_data()
    response_1 = TaxCategoryCall.create(headers, data)
    log_request_response(EndpointTaxCategory.tax_category(), response_1, headers, data)
    AssertionStatusCode.assert_status_code_201(response_1)
    created_tax_categories.append(response_1.json())
    response_2 = TaxCategoryCall.create(headers, data)
    log_request_response(EndpointTaxCategory.tax_category(), response_2, headers, data)
    AssertionStatusCode.assert_status_code_422(response_2)



"""
TC150 - Negativo: No debe permitir crear una categoría con token inválido (401 Unauthorized).
"""
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC150_creacion_con_token_invalido():
    data = generate_tax_category_data()
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = TaxCategoryCall.create(invalid_headers, data)
    log_request_response(EndpointTaxCategory.tax_category(), response, invalid_headers, data)
    AssertionStatusCode.assert_status_code_401(response)


"""
TC68 - Negativo: El sistema debe rechazar la creación de categoría si no se proporciona token de autenticación (HTTP 401).
"""
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC68_creacion_sin_autenticacion():
    data = generate_tax_category_data()
    empty_headers = {}
    response = TaxCategoryCall.create(empty_headers, data)
    log_request_response(EndpointTaxCategory.tax_category(), response, empty_headers, data)
    AssertionStatusCode.assert_status_code_401(response)


"""
TC63 - Validación de encabezados: La respuesta al crear una categoría de impuesto debe incluir 
el encabezado 'Content-Type' y su valor debe comenzar con 'application/ld+json'.
"""
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
@pytest.mark.functional
@pytest.mark.smoke
def test_TC65_validar_limite_longitud_code(auth_headers):
    data = generate_tax_category_data()
    data["code"] = "A" * 256
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(
        url=EndpointTaxCategory.tax_category(),
        response=response,
        headers=auth_headers
    )
    AssertionStatusCode.assert_status_code_422(response)



"""
TC66 - Negativo: Validar que el sistema rechaza la creación de una categoría de impuesto
cuando el campo 'code' contiene caracteres especiales no permitidos como '@', '#', '%'.
"""
@pytest.mark.functional
@pytest.mark.smoke
def test_TC66_validar_caracteres_especiales_en_code(auth_headers):
    data = generate_tax_category_data()
    data["code"] = "ABC@#%"
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(url=EndpointTaxCategory.tax_category(), response=response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_422(response)


"""
TC67 - Validar que el sistema permite la creación de una categoría de impuesto
con el campo 'description' vacío.
"""
@pytest.mark.functional
@pytest.mark.smoke
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
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC221_creacion_sin_nombre_categoria(auth_headers):
    data = generate_tax_category_data()
    data.pop("name", None)
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(url=EndpointTaxCategory.tax_category(), response=response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_422(response)


"""
No debe permitir crear una categoría con nombre menor a 2 caracteres (Sylius debe responder 422).
"""
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.parametrize("invalid_name", [
    "",    # vacío
    "A",   # un solo carácter
])
def test_TC255_tax_category_name_min_length(setup_add_tax_category, invalid_name):

    auth_headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_data()
    data["name"] = invalid_name
    url = EndpointTaxCategory.tax_category()
    response = TaxCategoryCall.create(auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)
    log_request_response(url, response, auth_headers)


"""
TC-220No debe permitir crear una categoría de impuesto con un nombre mayor a 255 caracteres.
Sylius debe responder con un código de estado HTTP 422.
"""
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.negative
def test_TC220_tax_category_name_exceeds_max_length(setup_add_tax_category):
    auth_headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_data()
    data["name"] = "A" * 256  # 256 caracteres
    url = EndpointTaxCategory.tax_category()
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(url, response, auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)


"""
No debe permitir crear una categoría de impuesto si el nombre solo contiene
espacios en blanco, saltos de línea u otros caracteres invisibles. Sylius debe responder con 422.
"""
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.xfail(reason="known issue La app permite espacios vacios BUG", run=False)
@pytest.mark.parametrize("invalid_name", [
    "   ",
    "\n",
    "\n\n",
    " \n ",
    "\t",
    " \t \n "
])

def test_TC221_tax_category_name_whitespace_only(setup_add_tax_category, invalid_name):

    auth_headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_data()
    data["name"] = invalid_name
    url = EndpointTaxCategory.tax_category()
    response = TaxCategoryCall.create(auth_headers, data)
    log_request_response(url, response, auth_headers, data)
    AssertionStatusCode.assert_status_code_422(response)