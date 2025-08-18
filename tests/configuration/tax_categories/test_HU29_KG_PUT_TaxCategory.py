import pytest

from src.assertions.TaxCategory_assertions.taxCategory_schema_assertions import AssertionTaxCategory
from src.assertions.TaxCategory_assertions.tax_category_post_content_assertions import AssertionTaxCategoryCreate
from src.assertions.TaxCategory_assertions.tax_category_errors_assertions import AssertionTaxCategoryErrors
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_tax_category import EndpointTaxCategory
from src.routes.request import SyliusRequest
from src.data.taxCategory import generate_tax_category_data
from utils.logger_helpers import log_request_response


#TC361 Admin > Configuration> Tax Category - Actualizacion completa de una categoria con campos validos
@pytest.mark.smoke
@pytest.mark.high
@pytest.mark.functional
def test_TC361_Editar_Actualizacion_completa_campos_validos(setup_edit_tax_category):
    headers, tax_category = setup_edit_tax_category
    url = EndpointTaxCategory.code(tax_category["code"])
    response_before = SyliusRequest.get(url, headers)
    AssertionTaxCategory.assert_tax_category_code_schema(response_before.json())
    log_request_response(url, response_before)
    payload = generate_tax_category_data()
    payload.pop("code")
    response = SyliusRequest.put(url, headers, payload)
    AssertionTaxCategory.assert_tax_category_edit_input_schema(payload)
    response_json = response.json()
    AssertionTaxCategory.assert_tax_category_output_schema(response_json)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxCategory.assert_tax_category_code_schema(response.json())
    log_request_response(url, response, headers, payload)



#TC362 Admin > Configuration> Tax Category - Actualizacion de categoria solo con campos obligatorios
@pytest.mark.smoke
@pytest.mark.high
@pytest.mark.functional
def test_TC362_Editar_campos_obligatorios_tax_category(setup_edit_tax_category):
    headers, tax_category = setup_edit_tax_category
    url = EndpointTaxCategory.code(tax_category["code"])
    response_before = SyliusRequest.get(url, headers)
    AssertionTaxCategory.assert_tax_category_code_schema(response_before.json())
    log_request_response(url, response_before)
    payload = generate_tax_category_data(required_only=True)
    payload.pop("code", None)
    response = SyliusRequest.put(url, headers, payload)
    AssertionTaxCategory.assert_tax_category_edit_input_schema(payload)
    response_json = response.json()
    AssertionTaxCategory.assert_tax_category_output_schema(response_json)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxCategory.assert_tax_category_code_schema(response_json)
    log_request_response(url, response, headers, payload)
    assert response_json["name"] == payload["name"], "El nombre no se actualizó correctamente"
    assert "description" in response_json, "La respuesta debería incluir el campo description"


#TC398 Admin > Configuration > Tax Category - Validar actualización de categoría con formato inválido en campo nombre
#TC363 Admin > Configuration> Tax Category - validar que al actualizar categoria no permita guardar campos vacios
@pytest.mark.high
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.xfail(reason="known issue La app permite espacios vacios y campos invalidos BUG", run=True)
@pytest.mark.parametrize("invalid_payload,expected_error,expected_status", [
    ({"name": ""}, "Please enter tax category name.", 422),
    ({"name": "   "}, None, 422), #en este caso deberia de fallar pero manda como bien con 200
    ({"name": None}, "The type of the \"name\" attribute must be \"string\"", 400),
    ({"name": "Válido", "description": ""}, None, 200),
    ({"name": "+"}, "solo dato invalido.", 400) #no ingresar con semantica incorrecta
])
def test_TC363_398_No_permitir_campos_vacios(setup_edit_tax_category, invalid_payload, expected_error, expected_status):
    headers, tax_category_data = setup_edit_tax_category
    url = EndpointTaxCategory.code(tax_category_data["code"])
    initial_response = SyliusRequest.get(url, headers)
    initial_data = initial_response.json()
    log_request_response(url, initial_response, headers)
    response = SyliusRequest.put(url, headers, invalid_payload)
    log_request_response(url, response, headers, invalid_payload)
    assert response.status_code == expected_status, f"Esperado status {expected_status}, obtenido {response.status_code}"
    response_json = response.json()

    if expected_error:
        mensaje = ""
        if "violations" in response_json:
            mensajes = [v["message"] for v in response_json["violations"]]
            mensaje = " ".join(mensajes)
        elif "detail" in response_json:
            mensaje = response_json["detail"]
        assert expected_error.lower() in mensaje.lower(), f"Mensaje esperado '{expected_error}' no encontrado en '{mensaje}'"
        current_response = SyliusRequest.get(url, headers)
        current_data = current_response.json()
        assert current_data["name"] == initial_data["name"], "El nombre no debería haber cambiado"
        assert current_data.get("description") == initial_data.get("description"), "La descripción no debería haber cambiado"
    else:
        current_response = SyliusRequest.get(url, headers)
        current_data = current_response.json()
        for k, v in invalid_payload.items():
            assert current_data[k] == v, f"El campo '{k}' debería haberse actualizado a '{v}'"




# TC396 Admin > Configuration > Tax Category - Actualización de categoría sin campos obligatorios
@pytest.mark.high
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.xfail(reason="known issue La app permite espacios vacios BUG", run=True)
def test_TC396_Actualizar_sin_campos_obligatorios_tax_category(setup_edit_tax_category):
    headers, tax_category_data = setup_edit_tax_category
    url = EndpointTaxCategory.code(tax_category_data["code"])
    initial_response = SyliusRequest.get(url, headers)
    initial_data = initial_response.json()
    log_request_response(url, initial_response, headers)
    payload = {}
    response = SyliusRequest.put(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    #assert response.status_code == 200, f"El backend debería responder 422, pero respondió {response.status_code}"
    current_response = SyliusRequest.get(url, headers)
    current_data = current_response.json()
    assert current_data["name"] == initial_data["name"], "El nombre no debería haber cambiado"
    assert current_data.get("description") == initial_data.get("description"), "La descripción no debería haber cambiado"



#TC397 Admin > Configuration > Tax Category - Validar actualización de categoría con formato inválido en campo nombre
@pytest.mark.functional
@pytest.mark.medium
@pytest.mark.negative
def test_TC397_Actualizar_nombre_caracter_especial_tax_category(setup_edit_tax_category):
    headers, tax_category_data = setup_edit_tax_category
    url = EndpointTaxCategory.code(tax_category_data["code"])
    response_before = SyliusRequest.get(url, headers)
    initial_data = response_before.json()
    AssertionTaxCategory.assert_tax_category_code_schema(initial_data)
    log_request_response(url, response_before, headers)
    payload = {"name": "@"}
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionTaxCategoryErrors.assert_min_length_error(response_json, "name")
    response_after = SyliusRequest.get(url, headers)
    current_data = response_after.json()
    assert current_data["name"] == initial_data["name"], "El nombre no debería haber cambiado con valor inválido '@'"


# TC398 Admin > Configuration > Tax Category - Intentar actualizar categorías inexistentes
@pytest.mark.functional
@pytest.mark.high
@pytest.mark.negative
def test_TC398_actualizacion_categoria_inexistente(setup_edit_tax_category):
    headers, tax_category = setup_edit_tax_category
    url = EndpointTaxCategory.code(f'{tax_category["code"]}x')  # Código modificado para asegurar que no existe
    payload = {"name": "Categoria Fantasma", "description": "Intento de actualización de categoría inexistente"}
    response = SyliusRequest.put(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionTaxCategoryErrors.assert_not_found_error(response.json(), 404, "Not Found")


#TC400 Admin > Configuration> Tax Category - intentar Aztualizar categorias con token invalido
@pytest.mark.functional
@pytest.mark.high
@pytest.mark.security
@pytest.mark.negative
def test_TC400_actualizacion_tax_category_sin_permisos(setup_edit_tax_category):
    headers, tax_category = setup_edit_tax_category
    # Token inválido/sin permisos (puedes ajustar el valor según el caso que quieras probar)
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTQzNjg3MTcsImV4cCI6MTc1NDM3MjMxNywicm9sZXMiOlsiUk9MRV9BRE1JTklTVFJBVElPTl9BQ0NFU1MiLCJST0xFX0FQSV9BQ0NFU1MiXSwidXNlcm5hbWUiOiJhcGkifQ.kCQgpWu-6UHG0hPiMacehDGUWBVf3L6R9MEkwujopo-lo6GkwEtXndnWgCyyzPQcZmoMuMAocDRT5NVaR1tU_YYPLi-haJ9dYuWe7-2vPz6wgPeOfuXWGnIbNKd-nrOZtLz8naX5xYRQAZdvkSVN6-tVfPHyKtQwcI-gii2mW1qQO2TwfVVQBHEwrrsRxuqKbkah4nPmICP4na8hM3svn2oYJA96knq6rfWcCEyCVAm3gRpyoFG-iyaYSJMPeRZvYa0Ua4HuWDaXnIYGGbAUuGOlyGpfOq5s1pAdSBSUPsOEYWRczQsCHwi6IEnKO9hNyNgKMfjW7B5ba3vmT6IZERhM_hjfNHW9s83Um0kLiMyMhkGW6PmsOTZdoIsyscUO1uhj6mHXi9fJ53lgyxIkbQSRadczj7cxCnHPtBrpCdiQrQgF8JW3wZJHe_GIDtWB67_0lf8Fs60ntPzIB2pVJIohC95OoqSzoVvLcKae9pGfmPJz0JLevtA9xXUwSkK8v9ixVEWSyJt89j8XVkZ6dqEFAR1qOAk9Uh9AZN9c3ImkLF7XHmlHHoJsFLuwpjEoGS5m4Ul7V0InPVHAI-ys_JVL3hPpVLBxlTr66l8j2wPTnCozNYS7w5-w-0pLtDy4ajMYjU2ICpci1VbJsCP-kzIrdIg2nz5PuO33v9SDyZg"}
    url = EndpointTaxCategory.code(tax_category["code"])
    payload = {"name": "Intento sin permisos", "description": "No debería permitir"}
    response = SyliusRequest.put(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxCategoryErrors.assert_tax_category_errors(response.json(), 401, "Expired JWT Token")



#TC399 Admin > Configuration> Tax Category - intentar actualizar categoria sin autenticacion
@pytest.mark.functional
@pytest.mark.high
@pytest.mark.negative
def test_TC399_actualizacion_tax_category_sin_autenticacion(setup_edit_tax_category):
    _, tax_category = setup_edit_tax_category
    url = EndpointTaxCategory.code(tax_category["code"])
    payload = {"name": "Intento sin auth", "description": "No debería permitir"}
    headers = {}  # Sin token
    response = SyliusRequest.put(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxCategoryErrors.assert_tax_category_errors(response.json(), 401, "JWT Token not found")



#TC 401 Admin > Configuration> Tax Category - validar que permita actualizar categoria solo un campo sin que afecte a los demas
@pytest.mark.functional
@pytest.mark.high
@pytest.mark.negative
def test_TC401_actualizacion_campo_unico_tax_category(setup_edit_tax_category):
    headers, tax_category = setup_edit_tax_category
    url = EndpointTaxCategory.code(tax_category["code"])
    nombre_original = tax_category["name"]
    descripcion_original = tax_category["description"]
    nuevo_nombre = nombre_original + "_edit"
    payload = {"name": nuevo_nombre}
    response = SyliusRequest.put(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    assert response_json["name"] == nuevo_nombre, "El nombre no fue actualizado correctamente."
    assert response_json["description"] == descripcion_original, "La descripción fue alterada y no debería cambiar."
    assert response_json["code"] == tax_category["code"], "El código fue alterado y no debería cambiar."



#TC417 Admin > Configuration > Tax Category -  validar que no permita editar codigo de categoria
@pytest.mark.functional
@pytest.mark.high
@pytest.mark.negative
def test_TC417_intento_actualizar_code_tax_category_insatisfactoriamente(setup_edit_tax_category):
    headers, tax_category = setup_edit_tax_category
    url = EndpointTaxCategory.code(tax_category["code"])
    response_before = SyliusRequest.get(url, headers)
    AssertionTaxCategory.assert_tax_category_code_schema(response_before.json())
    log_request_response(url, response_before)
    payload = tax_category.copy()
    payload["code"] = tax_category["code"] + "_nuevo"
    response = SyliusRequest.put(url, headers, payload)
    AssertionTaxCategory.assert_tax_category_edit_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxCategory.assert_tax_category_code_schema(response.json())
    log_request_response(url, response, headers, payload)
    assert response.json()["code"] == tax_category["code"], "El código fue alterado y no debería cambiar."



#TC403 Admin > Configuration> Tax Category - Verificar que no permita actualizar con nombre muy largo sobrepasando los 255 caracteres
@pytest.mark.functional
@pytest.mark.medium
@pytest.mark.negative
def test_TC403_actualizacion_nombre_tax_category_demasiado_largo(setup_edit_tax_category):
    headers, tax_category = setup_edit_tax_category
    url = EndpointTaxCategory.code(tax_category["code"])
    nombre_largo = "X" * 256
    payload = {"name": nombre_largo}
    response = SyliusRequest.put(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionTaxCategoryErrors.assert_max_length_error(response.json(), "name")


#TC404 Admin > Configuration> Tax Category - Validar que no permita actualizar con valores null
@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.high
def test_TC404_actualizacion_tax_category_con_valores_null(setup_edit_tax_category):
    headers, tax_category = setup_edit_tax_category
    url = EndpointTaxCategory.code(tax_category["code"])
    payload = {
        "name": None,
        "description": None
    }
    response = SyliusRequest.put(url, headers, payload)
    log_request_response(url, response, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)

