import requests

url = "https://postman-rest-api-learner.glitch.me//objects?id=ff8081819782e69e019839a42b43708c"

response = requests.request("GET", url)

assert response.status_code == 410
"""
ID: DS001-13

Título:
Obtener los datos del objeto 436121

Descripción:
El usuario debe obtener los datos de título, artista, fecha de creación, imagen principal, y demás campos relevantes.
(e.g. Prueba de llamada por Postman)

Precondiciones:
1. El objeto debe existir en la colección del MET API.
   - objectID = 436121
2. Acceso a: https://collectionapi.metmuseum.org
3. Usuario con acceso a internet y a Postman (no requiere autenticación).

Ambiente:
- Navegador o cliente API: Postman
- URL base: https://collectionapi.metmuseum.org
- Endpoint específico: /public/collection/v1/objects/436121

Pasos:
1. Abrir Postman.
2. Copiar y pegar la siguiente URL:
   https://collectionapi.metmuseum.org/public/collection/v1/objects/436121
3. Seleccionar el método: GET
4. Hacer clic en el botón “Send”.
5. Verificar que el status code sea 200 OK.
6. Comparar la salida con los siguientes campos:

   - objectID = 436121
   - title = "Young Mother Sewing"
   - artistDisplayName = "Mary Cassatt"
   - objectDate = "1900"
   - primaryImage contiene una URL válida (string no vacío)

Resultado Esperado:
{
  "objectID": 436121,
  "title": "Young Mother Sewing",
  "artistDisplayName": "Mary Cassatt",
  "objectDate": "1900",
  "primaryImage": "https://images.metmuseum.org/CRDImages/ep/original/DP-13109-001.jpg",
  ...
}

Evidencias:
- Captura de pantalla en Postman mostrando:
  - Método GET
  - URL
  - Body de respuesta
  - Status code 200

CURL (opcional):
curl --location --request GET 'https://collectionapi.metmuseum.org/public/collection/v1/objects/436121'

Prioridad:
3 – Medium

Postcondición (Tierdown):
No aplica (GET no crea ni modifica datos)
"""