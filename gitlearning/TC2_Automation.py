import pytest
import requests
@pytest.mark.smoke

#Tarea 2 > Test Automation tipos de respuesta HTTP - 404

def test_0001_Obtener_el_response_404_de_un_objeto_eliminado():

#Desscripcion: Verificar que se muestre status code 404 cuando se intenta obtener la informacion
# de un item eliminado en la aplicacion todo ly

#Ambiente
 url = "https://todo.ly/api/items/[1].format"

#Pasos
#1. Abrir Postman
#2. Copiar la URL
#3. Seleccionar GET
 list_url = url + 'objects'

#4. Clic en el botón Send
 response = requests.get(list_url)

# 5. Verificar el status code del response
 assert response.status_code == 404


#Tarea 2 > Test Automation tipos de respuesta HTTP - 400

def test_0001_Obtener_el_response_400_de_un_objeto_invalido():

#Desscripcion: Verificar que se muestre status code 400 cuando se intenta obtener la informacion
# de un item invalido en la aplicacion todo ly

#Ambiente
 url = "https://todo.ly/api/items/[invalid_item].format"

#Pasos
#1. Abrir Postman
#2. Copiar la URL
#3. Seleccionar GET
 list_url = url + 'objects'

#4. Clic en el botón Send
 response = requests.get(list_url)

# 5. Verificar el status code del response
 assert response.status_code == 400