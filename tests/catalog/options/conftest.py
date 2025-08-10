import pytest

from src.resources.call_request.options_call import OptionsCall

@pytest.fixture(scope="function")
def setup_add_options(auth_headers):
    created_options = []
    yield auth_headers, created_options

    for option in created_options:
        if 'code' in option:
            OptionsCall().delete(auth_headers, option['code'])
        else:
            print(f"La opción de producto no tiene 'code': {option}")
