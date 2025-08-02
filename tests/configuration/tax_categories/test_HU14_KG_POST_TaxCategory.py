import pytest
import requests
from faker import Faker

from utils.config import BASE_URL
from src.assertions.taxCategory_assertions import AssertionTaxCategory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.data.taxCategory import generate_tax_category_source_data


def test_TC60_Crear_categoría_de_impuesto_exitosamente(auth_headers):
    """
    Validar que la API permita crear una categoría de impuesto cuando se envían datos válidos.
    """
    url = f"{BASE_URL}/admin/tax-categories"
    data = generate_tax_category_source_data()
    response = requests.post(url, json=data, headers=auth_headers)
    AssertionTaxCategory.assert_tax_category_input_schema(data)
    AssertionStatusCode.assert_status_code_201(response)
    AssertionTaxCategory.assert_tax_category_output_schema(response.json())



@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC62_error_por_codigo_duplicado(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    data = generate_tax_category_source_data()
    # Crear la primera categoría
    response_1 = requests.post(url, json=data, headers=auth_headers)
    AssertionStatusCode.assert_status_code_201(response_1)
    # Intentar crearla nuevamente con el mismo código
    response_2 = requests.post(url, json=data, headers=auth_headers)
    AssertionStatusCode.assert_status_code_422(response_2)
    assert "violations" in response_2.json()



@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC150_creacion_con_token_invalido():
    url = f"{BASE_URL}/admin/tax-categories"
    data = generate_tax_category_source_data()
    invalid_headers = {"Authorization": "Bearer invalid_token"}

    response = requests.post(url, json=data, headers=invalid_headers)
    AssertionStatusCode.assert_status_code_401(response)




@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.smoke
def test_TC68_creacion_sin_autenticacion():
    url = f"{BASE_URL}/admin/tax-categories"
    data = generate_tax_category_source_data()
    response = requests.post(url, json=data)  # sin headers
    AssertionStatusCode.assert_status_code_401(response)


@pytest.mark.functional
@pytest.mark.smoke
def test_TC63_verificar_encabezados_respuesta(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    data = generate_tax_category_source_data()
    response = requests.post(url, json=data, headers=auth_headers)
    AssertionStatusCode.assert_status_code_201(response)
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"].startswith("application/ld+json")


@pytest.mark.functional
@pytest.mark.smoke
def test_TC64_verificar_formato_y_tipos_datos_en_respuesta(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    data = generate_tax_category_source_data()
    response = requests.post(url, json=data, headers=auth_headers)
    AssertionStatusCode.assert_status_code_201(response)
    res_json = response.json()
    assert isinstance(res_json["code"], str)
    assert isinstance(res_json["name"], str)
    assert isinstance(res_json["description"], str)


@pytest.mark.functional
@pytest.mark.smoke
def test_TC65_validar_limite_longitud_code(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    data = generate_tax_category_source_data()
    data["code"] = "A" * 256  # suponiendo que el límite es < 256
    response = requests.post(url, json=data, headers=auth_headers)
    AssertionStatusCode.assert_status_code_400_or_422(response)


@pytest.mark.functional
@pytest.mark.smoke
def test_TC66_validar_caracteres_especiales_en_code(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    data = generate_tax_category_source_data()
    data["code"] = "ABC@#%"
    response = requests.post(url, json=data, headers=auth_headers)
    AssertionStatusCode.assert_status_code_400_or_422(response)



@pytest.mark.functional
@pytest.mark.smoke
def test_TC67_description_vacio(auth_headers):
    url = f"{BASE_URL}/admin/tax-categories"
    data = generate_tax_category_source_data()
    data["description"] = ""
    response = requests.post(url, json=data, headers=auth_headers)
    # Asume que el campo es requerido. Si no lo es, debe cambiarse la validación:
    AssertionStatusCode.assert_status_code_400_or_422(response)