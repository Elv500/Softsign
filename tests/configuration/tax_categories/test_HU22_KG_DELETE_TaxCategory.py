import logging
import pytest
import time
import threading

from src.routes.request import SyliusRequest
from src.assertions.taxCategory_assertions import AssertionTaxCategory
from src.assertions.status_code_assertions import AssertionStatusCode
from src.data.taxCategory import generate_tax_category_data
from src.routes.endpoint_tax_category import EndpointTaxCategory
from src.resources.call_request.taxCategory_call import TaxCategoryCall
from utils.logger_helpers import log_request_response


#Admin > Configuration  >Tax Category - Eliminar Tax Category exitosamente
@pytest.mark.functional
@pytest.mark.regression
def test_TC75_eliminar_TaxCategory(auth_headers):
    initial_data = generate_tax_category_data()
    create_endpoint = EndpointTaxCategory.tax_category()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)

    tax_category_code = create_response.json().get("code")
    endpoint = EndpointTaxCategory.code(tax_category_code)
    response = SyliusRequest.delete(endpoint, auth_headers)
    log_request_response(endpoint, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(response)



# Admin > Configuration > Tax Categories  – Validar error al eliminar categoría inexistente
@pytest.mark.functional
@pytest.mark.regression
def test_TC76_eliminar_TaxCategories_inexistente(auth_headers):
    fake_code = "Tax_no_existe-234+"
    endpoint = EndpointTaxCategory.code(fake_code)
    response = SyliusRequest.get(endpoint, auth_headers)
    log_request_response(endpoint, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_404(response)



# Admin > Configuration > Tax Categories – Validar rechazo al eliminar con token inválido o sin permisos
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.regression
def test_TC80_eliminar_TaxCategory_sin_token():
    fake_code = "no existe"
    endpoint = EndpointTaxCategory.code(fake_code)
    response = SyliusRequest.delete(endpoint,headers={})
    log_request_response(endpoint, response)
    AssertionStatusCode.assert_status_code_401(response)



# Admin > Configuration > Tax Category - TC_03 Validar respuesta sin cuerpo en eliminación exitosa
@pytest.mark.functional
@pytest.mark.regression
def test_eliminar_TaxCategory_respuesta_sin_cuerpo(auth_headers):
    initial_data = generate_tax_category_data()
    create_endpoint = EndpointTaxCategory.tax_category()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    tax_category_code = create_response.json().get("code")

    endpoint = EndpointTaxCategory.code(tax_category_code)
    response = SyliusRequest.delete(endpoint, auth_headers)
    log_request_response(endpoint, response, headers=auth_headers)

    AssertionStatusCode.assert_status_code_204(response)
    #validar que no tenga cuerpo
    assert not response.content or response.content == b'', "La respuesta de eliminación debería estar vacía (sin body)"



# Admin > Configuration > Tax Category - TC_04 Validar requerimiento de autenticación para eliminar categoría
@pytest.mark.functional
@pytest.mark.regression
def test_requerimiento_autenticacion_eliminar_TaxCategory():
    fake_code = "TAX-AUTH-REQ-12345"
    invalid_headers = {"AUTHORIZATION": "Bearer TOKEN_invalido"}
    endpoint = EndpointTaxCategory.code(fake_code)

    response = SyliusRequest.delete(endpoint, invalid_headers)
    log_request_response(endpoint, response, headers=invalid_headers)
    AssertionStatusCode.assert_status_code_401(response)



# Admin > Configuration - Tax Category - Verificar que el tiempo de respuesta al eliminar sea menor a 3 segundos
@pytest.mark.functional
@pytest.mark.performance
@pytest.mark.regression
def test__TC337_eliminar_CustomerGroup_tiempo_respuesta(auth_headers):
    # Crear un customer group para eliminar
    initial_data = generate_tax_category_data()
    create_endpoint = EndpointTaxCategory.tax_category()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    tax_category_code = create_response.json().get("code")


    delete_url = EndpointTaxCategory.code(tax_category_code)
    start_time = time.time()
    response = SyliusRequest.delete(delete_url, auth_headers)
    end_time = time.time()
    elapsed = end_time - start_time

    log_request_response(delete_url, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(response)
    assert elapsed < 3, f"El tiempo de respuesta fue {elapsed:.2f}s, debería ser menor a 3 segundos"



# Admin > Configuration > Tax Category -  Verificar headers de respuesta al eliminar
@pytest.mark.functional
@pytest.mark.regression
def test_TC338_eliminar_TaxCategory_headers_respuesta(auth_headers):
    # Crear una tax category para eliminar
    data = generate_tax_category_data()
    create_endpoint = EndpointTaxCategory.tax_category()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)
    tax_category_code = create_response.json().get("code")

    endpoint = EndpointTaxCategory.code(tax_category_code)
    response = SyliusRequest.delete(endpoint, auth_headers)
    log_request_response(endpoint, response, headers=auth_headers)

    AssertionStatusCode.assert_status_code_204(response)

    # Verificar headers importantes de la respuesta
    assert response.content == b"" or len(response.content) == 0


# Admin > Configuration > Tax Category -  Verificar que el grupo eliminado no exista más
@pytest.mark.functional
@pytest.mark.regression
def test_TC339_eliminar_TaxCategory_verificar_no_existe(auth_headers):
    initial_data = generate_tax_category_data()
    create_endpoint = EndpointTaxCategory.tax_category()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    tax_category_code = create_response.json().get("code")
    #eliminar
    endpoint = EndpointTaxCategory.code(tax_category_code)
    delete_response = SyliusRequest.delete(endpoint, auth_headers)
    log_request_response(endpoint, delete_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)
    # Verificar que ya no exista
    get_deleted_response = SyliusRequest.get(endpoint, auth_headers)
    log_request_response(endpoint, get_deleted_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_404(get_deleted_response)


# Admin > Configuration > Tax Category - Verificar que no permita eliminar la misma categoría dos veces
@pytest.mark.functional
@pytest.mark.regression
def test_TC340_eliminar_TaxCategory_doble_eliminacion(auth_headers):
    initial_data = generate_tax_category_data()
    create_endpoint = EndpointTaxCategory.tax_category()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    tax_category_code = create_response.json().get("code")
    # Eliminar
    endpoint = EndpointTaxCategory.code(tax_category_code)
    first_delete_response = SyliusRequest.delete(endpoint, auth_headers)
    log_request_response(endpoint, first_delete_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(first_delete_response)
    # Eliminar 2 (debe fallar con 404)
    second_delete_response = SyliusRequest.delete(endpoint, auth_headers)
    log_request_response(endpoint, second_delete_response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_404(second_delete_response)


# Admin > Configuration > Tax Category - Verificar eliminación de múltiples grupos secuencialmente
@pytest.mark.functional
@pytest.mark.regression
def test__TC341eliminar_multiples_TaxCategory_secuencialmente(auth_headers):

    tax_categories = []
    for i in range(3):
        data = generate_tax_category_data(name=f"CategoriaTest{i}")
        create_endpoint = EndpointTaxCategory.tax_category()
        create_response = SyliusRequest.post(create_endpoint, auth_headers, data)
        AssertionStatusCode.assert_status_code_201(create_response)
        code = create_response.json().get("code")
        tax_categories.append(code)

    # Eliminar cada tax category secuencialmente y verificar que ya no existen
    for code in tax_categories:
        endpoint = EndpointTaxCategory.code(code)
        delete_response = SyliusRequest.delete(endpoint, auth_headers)
        log_request_response(endpoint, delete_response, headers=auth_headers)
        AssertionStatusCode.assert_status_code_204(delete_response)

        # Verificar que la categoría eliminada ya no existe
        get_deleted_response = SyliusRequest.get(endpoint, auth_headers)
        log_request_response(endpoint, get_deleted_response, headers=auth_headers)
        AssertionStatusCode.assert_status_code_404(get_deleted_response)



# Admin > Configuration > Tax Category -  Verificar eliminación concurrente de la misma categoría
@pytest.mark.functional
@pytest.mark.regression
def test_TC342_eliminar_TaxCategory_concurrente(auth_headers):
    # Crear una tax category para eliminar
    initial_data = generate_tax_category_data()
    create_endpoint = EndpointTaxCategory.tax_category()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    tax_category_code = create_response.json().get("code")

    endpoint = EndpointTaxCategory.code(tax_category_code)
    results = []

    def concurrent_delete():
        response = SyliusRequest.delete(endpoint, auth_headers)
        log_request_response(endpoint, response, headers=auth_headers)
        results.append(response)

    # Ejecutar dos eliminaciones concurrentes
    thread1 = threading.Thread(target=concurrent_delete)
    thread2 = threading.Thread(target=concurrent_delete)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # Analizar resultados: solo uno debe ser exitoso (204), el otro debe ser 404
    status_codes = sorted([r.status_code for r in results])
    assert status_codes == [204, 404], f"Se esperaban los códigos [204, 404], se obtuvieron: {status_codes}"





# Admin > Configuration > Tax Category - TC_10 Verificar que la eliminación de un tax category no impacta otros existentes
@pytest.mark.functional
@pytest.mark.regression
def test_TC343_eliminar_TaxCategory_no_impacta_otros(auth_headers):
    data_1 = generate_tax_category_data(name="CategoriaA")
    data_2 = generate_tax_category_data(name="CategoriaB")
    endpoint_create = EndpointTaxCategory.tax_category()

    response_1 = SyliusRequest.post(endpoint_create, auth_headers, data_1)
    AssertionStatusCode.assert_status_code_201(response_1)
    code_1 = response_1.json().get("code")

    response_2 = SyliusRequest.post(endpoint_create, auth_headers, data_2)
    AssertionStatusCode.assert_status_code_201(response_2)
    code_2 = response_2.json().get("code")

    endpoint_delete_1 = EndpointTaxCategory.code(code_1)
    delete_response_1 = SyliusRequest.delete(endpoint_delete_1, auth_headers)
    log_request_response(endpoint_delete_1, delete_response_1, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response_1)

    endpoint_get_2 = EndpointTaxCategory.code(code_2)
    get_response_2 = SyliusRequest.get(endpoint_get_2, auth_headers)
    log_request_response(endpoint_get_2, get_response_2, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(get_response_2)
    assert get_response_2.json().get(
        "code") == code_2, "El tax category restante no debe verse afectado por la eliminación de otro"