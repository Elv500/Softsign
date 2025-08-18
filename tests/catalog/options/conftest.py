import pytest

from src.data.options import generate_options_source_data
from src.resources.call_request.options_call import OptionsCall
from src.resources.payloads.payload_options import PayloadOptions

@pytest.fixture(scope="module")
def setup_teardown_view_options(auth_headers):
    payload_options1 = PayloadOptions.build_payload_options(generate_options_source_data())
    payload_options2 = PayloadOptions.build_payload_options(generate_options_source_data())
    option1 = OptionsCall.create(auth_headers, payload_options1)
    option2 = OptionsCall.create(auth_headers, payload_options2)

    yield auth_headers, option1, option2

    OptionsCall().delete(auth_headers, option1['code'])
    OptionsCall().delete(auth_headers, option2['code'])

@pytest.fixture(scope="function")
def setup_add_options(auth_headers):
    created_options = []
    yield auth_headers, created_options

    for option in created_options:
        if 'code' in option:
            OptionsCall().delete(auth_headers, option['code'])
        else:
            print(f"La opción de producto no tiene 'code': {option}")

@pytest.fixture(scope="function")
def setup_options_cleanup(auth_headers):
    options_to_cleanup = []

    def add_option_for_cleanup(option_code):
        """Agregar un código de opción para limpieza posterior"""
        options_to_cleanup.append(option_code)

    yield auth_headers, add_option_for_cleanup

    for option_code in options_to_cleanup:
        try:
            OptionsCall().delete(auth_headers, option_code)
            print(f"Opción limpiada: {option_code}")
        except Exception as e:
            print(f"Error durante cleanup de {option_code}: {e}")