import pytest
import requests


from src.assertions.attributes_assertions import AssertionAttributes
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_attributes import EndpointAttributes
from src.routes.request import SyliusRequest
from src.data.attributes import generate_attributes_source_data
from tests.catalog.attributes.conftest import setup_attributes_cleanup
from utils.logger_helpers import log_request_response


#Admin> Catalog> Attributes TC_47: No se debe permitir actualizar si el atributo no existe.
@pytest.mark.negative
@pytest.mark.regression
def test_TC47_Verificar_que_no_permitar_actualizar_un_atributo_inexistente(auth_headers):
    update_data = generate_attributes_source_data()
    url = EndpointAttributes.code("codigo_inexistente_123")
    put_response = SyliusRequest.put(url, auth_headers, update_data)
    log_request_response(url, put_response, headers=auth_headers, payload=update_data)
    AssertionStatusCode.assert_status_code_404(put_response)


#Admin> Catalog> Attributes TC_48: No se debe permitir actualizar un atributo sin token.
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.smoke
def test_TC48_Verificar_que_no_se_permita_actualizar_atributo_sin_token():
    update_data = generate_attributes_source_data()
    url = EndpointAttributes.code("codigo_inexistente_123")
    put_response = SyliusRequest.put(url, {}, update_data)
    log_request_response(url, put_response, headers={}, payload=update_data)
    AssertionStatusCode.assert_status_code_401(put_response)


#Admin> Catalog> Attributes TC_233: No se debe actualizar el atributo con data invalida.
@pytest.mark.negative
@pytest.mark.smok
def test_TC233_Verificar_que_no_se_actualice_atributo_con_datos_invalidos(auth_headers):
    data = generate_attributes_source_data()
    post_response = SyliusRequest.post(EndpointAttributes.attributes(), auth_headers, data)
    AssertionStatusCode.assert_status_code_201(post_response)
    code = post_response.json()["code"]

    update_data = data.copy()
    update_data["translations"]["en_US"]["name"] = ""
    url = EndpointAttributes.code(code)
    put_response = SyliusRequest.put(url, auth_headers, update_data)
    log_request_response(url, put_response, headers=auth_headers, payload=update_data)
    AssertionStatusCode.assert_status_code_422(put_response)


# Admin> Catalog> Attributes> TC_44: Se permite actualizar un atributo con datos validos.
@pytest.mark.positive
@pytest.mark.functional
def test_TC44_Verificar_se_actualice_attributo_con_datos_validos(setup_attributes_cleanup):
    auth_headers, add_attributes_for_cleanup = setup_attributes_cleanup
    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    create_response = SyliusRequest.post(url, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)

    attribute = create_response.json()
    update_data = {**attribute}
    update_data["translations"] = {
        "en_US": {"name": "Updated Attributes Name"}
    }

    if attribute["type"] == "text":
        update_data["configuration"] = {
            "minCharacters": None,
            "maxCharacters": None
        }
    AssertionAttributes.assert_attributes_put_input_schema(update_data)


# Admin> Catalog> Attributes> TC_46: No se debe permitir actualizar un atributo sin el campo name.
@pytest.mark.negative
@pytest.mark.Functional
@pytest.mark.regression
def test_TC46_Verificar_actualizar_grupo_sin_el_campo_name(setup_attributes_cleanup):
    auth_headers, add_attributes_for_cleanup = setup_attributes_cleanup

    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    create_response = SyliusRequest.post(url, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)

    attributes_code = create_response.json()["code"]
    add_attributes_for_cleanup(attributes_code)

    update_data = {}
    endpoint = EndpointAttributes.code(attributes_code)
    response = SyliusRequest.put(endpoint, auth_headers, update_data)

    log_request_response(endpoint, response, headers=auth_headers, payload=update_data)
    AssertionStatusCode.assert_status_code_200(response)  # <-- Cambia aquí
    get_response = SyliusRequest.get(endpoint, auth_headers)
    assert get_response.json()["translations"]["en_US"]["name"] == data["translations"]["en_US"]["name"]



# Admin> Catalog> Attributes> TC_249: Se permite actualizar un atributo con caracteres especiales en el campo name.
@pytest.mark.functional
@pytest.mark.regression
def test_TC249_Verificar_actualizar_atributo_con_caracteres_especiales_en_name(setup_attributes_cleanup):
    auth_headers, add_attributes_for_cleanup = setup_attributes_cleanup

    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    create_response = SyliusRequest.post(url, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)

    attributes_code = create_response.json()["code"]
    add_attributes_for_cleanup(attributes_code)

    update_data = {
        "name": "updateName 66$@$@#"
    }
    endpoint = EndpointAttributes.code(attributes_code)
    response = SyliusRequest.put(endpoint, auth_headers, update_data)

    log_request_response(endpoint, response, headers=auth_headers, payload=update_data)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionAttributes.assert_attributes_put_output_schema(response.json())


# Admin> Catalog> Attributes> TC_250: No se permite actualizar un atributo si la autenticacion del token fallo.
@pytest.mark.negative
@pytest.mark.security
@pytest.mark.regression
def test_TC250_Verificar_no_actualizar_attribute_con_token_invalido():
    codigo_existente = "retail"
    data = {
        "name": "Nombre Actualizado Token Inválido"
    }
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    endpoint = EndpointAttributes.code(codigo_existente)
    response = SyliusRequest.put(endpoint, invalid_headers, data)

    log_request_response(endpoint, response, headers=invalid_headers, payload=data)
    AssertionStatusCode.assert_status_code_401(response)


# Admin> Catalog> Attributes> TC_251: No se permite actualizar un atributo si el body-json es incorrecto.
@pytest.mark.negative
@pytest.mark.regression
def test_TC251_Verificar_actualizar_atributo_json_body_incompleto(setup_attributes_cleanup):
    auth_headers, add_attributes_for_cleanup = setup_attributes_cleanup

    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    create_response = SyliusRequest.post(url, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)

    attributes_code = create_response.json()["code"]
    add_attributes_for_cleanup(attributes_code)

    endpoint = EndpointAttributes.code(attributes_code)
    response = requests.put(
        endpoint,
        headers={**auth_headers, 'Content-Type': 'application/json'},
        data='{"name": invalid_json}'
    )

    log_request_response(endpoint, response, headers={**auth_headers, 'Content-Type': 'application/json'})
    AssertionStatusCode.assert_status_code_400(response)


# Admin> Catalog> Attributes> TC_354: No see permite actualizar un atributo si el content type es incorrecto.
@pytest.mark.negative
@pytest.mark.regression
def test_TC354_Verificar_actualizar_atributo_con_content_type_incorrecto(setup_attributes_cleanup):
    auth_headers, add_attributes_for_cleanup = setup_attributes_cleanup

    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    create_response = SyliusRequest.post(url, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)

    attributes_code = create_response.json()["code"]
    add_attributes_for_cleanup(attributes_code)

    data = {
        "name": "Nombre Actualizado"
    }
    headers_with_text = auth_headers.copy()
    headers_with_text['Content-Type'] = 'text/plain'
    endpoint = EndpointAttributes.code(attributes_code)

    response = requests.put(
        endpoint,
        headers=headers_with_text,
        data=str(data)
    )

    log_request_response(endpoint, response, headers=headers_with_text)
    AssertionStatusCode.assert_status_code_415(response)


# Admin> Catalog> Attributes> TC_353: Validar los header de respuesta despues de la actualizacion del atributo.
@pytest.mark.functional
@pytest.mark.regression
def test_TC353_Verificar_headers_response_despues_actualizar_attribute(setup_attributes_cleanup):
    auth_headers, add_attributes_for_cleanup = setup_attributes_cleanup
    data = generate_attributes_source_data()
    url = EndpointAttributes.attributes()
    create_response = SyliusRequest.post(url, auth_headers, data)
    AssertionStatusCode.assert_status_code_201(create_response)

    attributes_code = create_response.json()["code"]
    add_attributes_for_cleanup(attributes_code)

    update_data = {
        "name": "Nombre Actualizado Headers"
    }
    endpoint = EndpointAttributes.code(attributes_code)
    response = SyliusRequest.put(endpoint, auth_headers, update_data)

    log_request_response(endpoint, response, headers=auth_headers, payload=update_data)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionAttributes.assert_attributes_put_output_schema(response.json())

    headers = response.headers
    content_type = headers.get("Content-Type", "")
    assert content_type.startswith("application/ld+json"), f"Expected JSON-LD content type, got: {content_type}"



