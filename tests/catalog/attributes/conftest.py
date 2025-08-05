import pytest

from src.resources.call_request.attributes_call import AttributesCall


@pytest.fixture(scope="function")
def setup_add_attributes(auth_headers):
    created_attributes = []
    yield auth_headers, created_attributes

    for attributes in created_attributes:
        if 'code' in attributes:
            AttributesCall().delete(auth_headers, attributes['code'])
        else:
            print(f"La fuente de attributes no tiene 'code': {attributes}")