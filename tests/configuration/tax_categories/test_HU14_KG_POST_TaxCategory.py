import pytest

from src.routes.request import SyliusRequest
from src.assertions.taxCategory_assertions import AssertionTaxCategory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.data.taxCategory import generate_tax_category_source_data
from src.routes.endpoint_tax_category import EndpointTaxCategory
from src.resources.call_request.taxCategory_call import TaxCategoryCall

@pytest.mark.smoke
@pytest.mark.functional
def test_TC60_Crear_categoría_de_impuesto_exitosamente(setup_add_tax_category):
    headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_source_data()
    response = SyliusRequest().post(EndpointTaxCategory.tax_category(), headers, data)
    AssertionTaxCategory.assert_tax_category_input_schema(data)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxCategory.assert_tax_category_output_schema(response.json())
    created_category = response.json()
    created_tax_categories.append(created_category)


@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC62_error_por_codigo_duplicado(setup_add_tax_category):
    headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_source_data()
    created_category = TaxCategoryCall.create(headers, data)
    created_tax_categories.append(created_category)
    response_2 = TaxCategoryCall.create(headers, data)
    AssertionStatusCode.assert_status_code_422(response_2)
    res_json = response_2.json() if hasattr(response_2, "json") else response_2
    assert "violations" in res_json


@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC150_creacion_con_token_invalido():
    data = generate_tax_category_source_data()
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = TaxCategoryCall.create(invalid_headers, data)
    AssertionStatusCode.assert_status_code_401(response)


@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC68_creacion_sin_autenticacion():
    data = generate_tax_category_source_data()
    # No enviar headers
    response = TaxCategoryCall.create({}, data)
    AssertionStatusCode.assert_status_code_401(response)


@pytest.mark.functional
@pytest.mark.smoke
def test_TC63_verificar_encabezados_respuesta(setup_add_tax_category):
    headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_source_data()
    response = TaxCategoryCall.create(headers, data)
    AssertionStatusCode.assert_status_code_201(response)
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"].startswith("application/ld+json")
    created_tax_categories.append(response.json())


@pytest.mark.functional
@pytest.mark.smoke
def test_TC64_verificar_formato_y_tipos_datos_en_respuesta(setup_add_tax_category):
    headers, created_tax_categories = setup_add_tax_category
    data = generate_tax_category_source_data()
    response = TaxCategoryCall.create(headers, data)
    AssertionStatusCode.assert_status_code_201(response)
    res_json = response.json()
    assert isinstance(res_json["code"], str)
    assert isinstance(res_json["name"], str)
    assert isinstance(res_json["description"], str)
    created_tax_categories.append(res_json)


@pytest.mark.functional
@pytest.mark.smoke
def test_TC65_validar_limite_longitud_code(auth_headers):
    data = generate_tax_category_source_data()
    data["code"] = "A" * 256  # suponiendo que el límite es < 256
    response = TaxCategoryCall.create(auth_headers, data)
    AssertionStatusCode.assert_status_code_400_or_422(response)

@pytest.mark.functional
@pytest.mark.smoke
def test_TC66_validar_caracteres_especiales_en_code(auth_headers):
    data = generate_tax_category_source_data()
    data["code"] = "ABC@#%"
    response = TaxCategoryCall.create(auth_headers, data)
    AssertionStatusCode.assert_status_code_400_or_422(response)

@pytest.mark.functional
@pytest.mark.smoke
def test_TC67_description_vacio(auth_headers):
    data = generate_tax_category_source_data()
    data["description"] = ""
    response = TaxCategoryCall.create(auth_headers, data)
    # Asume que el campo es requerido. Si no lo es, debe cambiarse la validación:
    AssertionStatusCode.assert_status_code_400_or_422(response)

@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TCXX_creacion_sin_nombre_categoria(auth_headers):
    data = generate_tax_category_source_data()
    data.pop("name", None)  # Eliminar el campo 'name'
    response = TaxCategoryCall.create(auth_headers, data)
    AssertionStatusCode.assert_status_code_400_or_422(response)


