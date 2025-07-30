import pytest
import requests

@pytest.mark.smoke
def test_001_obtener_la_lista_de_todos_los_departamentos():
#Descripción: El usuario desea obtener una lista con la información de todos los departamentos: El ID y Nombre.
# Ambiente:
    url = "https://collectionapi.metmuseum.org/public/collection/v1/departments"

    # Pasos:
    # 1. Ingresar a Postman
    # 2. Seleccionar GET
    # 3. Copiar la URL: https://collectionapi.metmuseum.org/public/collection/v1/departments
    # 4. Clic en Send
    response = requests.request("GET", url)
    # 5. Verificar la respuesta
    assert response.status_code == 200