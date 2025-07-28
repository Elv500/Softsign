import pytest
import requests

@pytest.mark.smoke
def test_0001_Obtener_la_lista_de_usuarios_registrados_en_el_menú_Admin():

#Desscripcion: Cuando el usuario administrador selecciona el menú “Admin” se debería
#listar los usuario registrados en la aplicación Orange HRM

#Ambiente
 url = "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers"

#Pasos
#1. Abrir Postman
#2. Copiar la URL
#3. Seleccionar GET
 list_url = url + 'objects'

#4. Clic en el botón Send
 response = requests.get(list_url)

# 5. Verificar el respuest
 assert response.status_code != 200