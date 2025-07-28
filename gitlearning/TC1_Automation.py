import requests
import pytest
# ID:TC_1
@pytest.mark.smoke
def test_001_obtener_la_lista_del_usuario_datos():
    """Descripcion: El usuario debe obtener la lista completa de todos los objetos existentes en el sistema"""
    url = "https://api.restful-api.dev/objects"
    response = requests.get(url)
    assert response.status_code == 200