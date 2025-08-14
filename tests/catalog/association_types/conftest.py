import pytest

from src.data.association_types import generate_association_types_source_data
from src.resources.call_request.association_types_call import AssociationTypesCall


@pytest.fixture(scope="function")
def teardown_association_types(auth_headers):
    created_association_types = []
    yield auth_headers, created_association_types

    for code in created_association_types:
        AssociationTypesCall().delete(auth_headers, code)
        
        
@pytest.fixture(scope="function")
def setup_association_types(auth_headers):
    payload = generate_association_types_source_data()
    association_type = AssociationTypesCall().create(auth_headers, payload)
    yield auth_headers, association_type
    if association_type:
        AssociationTypesCall().delete(auth_headers, association_type['code'])

        
@pytest.fixture(scope="module")
def setup_teardown_association_types(auth_headers):
    payload1 = generate_association_types_source_data()
    payload2 = generate_association_types_source_data()
    association_type1 = AssociationTypesCall().create(auth_headers, payload1)
    association_type2 = AssociationTypesCall().create(auth_headers, payload2)
    yield auth_headers, association_type1, association_type2
    AssociationTypesCall().delete(auth_headers, association_type1['code'])
    AssociationTypesCall().delete(auth_headers, association_type2['code'])