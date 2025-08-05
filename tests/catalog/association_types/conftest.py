import pytest

from src.resources.call_request.association_types_call import AssociationTypesCall


@pytest.fixture(scope="function")
def teardown_association_types(auth_headers):
    created_association_types = []
    yield auth_headers, created_association_types

    for code in created_association_types:
        AssociationTypesCall().delete(auth_headers, code)
