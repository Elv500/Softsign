import pytest
import requests

@pytest.mark.smoke

def test001_prueba():
    """Descripción: El usuario debe obtener los identificadores de todos los libros guardados disponibles"""

    # Ambiente
    url = "https://restful-booker.herokuapp.com/"

    lista_url = url + "booking"

    #response = requests.get(lista_url)
    response = requests.request("GET", lista_url)

    assert response.status_code == 200
