import pytest
import requests

"""
Titulo
- Obtener los identificadores de todos los libros
Descripción
- El usuario debe obtener los identificadores de todos los libros guardados disponibles
Precondiciones
- MÉTODO: GET
- URL: https://restful-booker.herokuapp.com/booking/
Ambiente
- Acceso a API Doc: https://restful-booker.herokuapp.com/apidoc/
Prioridad
- Media
Categoria
- Smoke
"""

@pytest.mark.smoke

def test001_Obtener_los_identificadores_de_todos_los_libros():
    """Descripción: El usuario debe obtener los identificadores de todos los libros guardados disponibles"""

    # Ambiente
    url = "https://restful-booker.herokuapp.com/booking"

    response = requests.request("GET", url)

    assert response.status_code == 200