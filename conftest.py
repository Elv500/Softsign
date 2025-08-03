import pytest
from utils.auth_token import get_token

@pytest.fixture(scope="session")
def auth_headers():
    """
    Devuelve un diccionario de headers con token válido.
    Útil para reutilizar en cualquier test que requiera autenticación.
    """
    token = get_token()
    return {'Authorization': f'Bearer {token}'}