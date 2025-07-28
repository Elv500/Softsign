import requests

# Esta prueba verifica que la API del Metropolitan Museum of Art
# responda correctamente al solicitar un objeto específico
# Asegura que el código de estado HTTP sea 200


def test_met_object_api_response_ok():
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/436121"

    headers = {
        'Cookie': 'incap_ses_1719_1662004=t9DCdCg0JnM9c1WZwR3bF+VLhGgAAAAA14Yp85ehzOHZpRVQuA012g==; visid_incap_1662004=OULm4zMJQJyHhBOS3Vy/QeVLhGgAAAAAQUIPAAAAAAD2CmFFkBWLnpdTy/inCV48'
    }

    response = requests.get(url, headers=headers)

    assert response.status_code == 200

"""
ID DS001-13
Titulo:
Obtener los datos del objeto 436121

Descripción
El usuario debe obtener los datos de título, artista, fecha de creación, imagen principal, y demás campos relevantes.
(e.g. Prueba de llamada por Postman)

Precondiciones
1. El objeto debe existir en la aplicación
e.g. 436121
(Como crear)

Ambiente
Acceso a collectionapi.metmuseum.org
Usuario con el que tienen acceso

Pasos
1. Acceder al login
2. Abrir postman
3. Copiar el URL
4. Seleccionar el metodo GET
5. Click en el boton send
6. Comparar la salida con los siguientes campos:
   - objectID = 436121
   - title = "Young Mother Sewing"
   - artistDisplayName = "Mary Cassatt"
   - objectDate = "1900"
   - primaryImage contiene url

Resultado Esperado
Body salida (Pegar de output o response)

Evidencias
Foto de postman
CURL

Prioridad
3 Medium

Post condition – Tierdown
No aplica (GET no crea datos)
"""