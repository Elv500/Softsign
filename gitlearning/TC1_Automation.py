import pytest
import requests



def test_get_character():

    url = "https://rickandmortyapi.com/api/character/171"


    response = requests.get(url)


    assert response.status_code == 200, f"Se esperaba código 200 pero se obtuvo {response.status_code}"

    data = response.json()
    assert isinstance(data, dict), "La respuesta no es un JSON válido"
    assert "id" in data, "El campo 'id' no está en la respuesta"
    assert data["id"] == 171, f"Se esperaba ID 171 pero se obtuvo {data['id']}"
    assert "name" in data, "El campo 'name' no está en la respuesta"
    assert "status" in data, "El campo 'status' no está en la respuesta"
    assert "species" in data, "El campo 'species' no está en la respuesta"


"""
Test Case: API > Get Character – Validar datos del personaje por ID
Descripción:
Verifica que al realizar una solicitud GET al endpoint https://rickandmortyapi.com/api/character/171, la API retorne una respuesta exitosa (código 200) y que el cuerpo del mensaje contenga campos clave como id, name, status, y species, además de que el ID corresponda al personaje solicitado.

Precondiciones:

Tener Postman instalado o entorno Python con requests y pytest.

Conexión a Internet.

La API de Rick and Morty debe estar disponible.

Prioridad: Alta

Tipo de prueba: Funcional

Datos de prueba:

URL: https://rickandmortyapi.com/api/character/171

Método: GET

| N° | Paso                                                                                  | Entrada           | Resultado Esperado                                |
| -- | ------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------- |
| 1  | Abrir Postman o ejecutar script Python                                                | N/A               | La herramienta está lista para enviar solicitudes |
| 2  | Enviar una solicitud GET al endpoint: `https://rickandmortyapi.com/api/character/171` | Método: `GET`     | Se recibe una respuesta de la API                 |
| 3  | Verificar el código de estado HTTP                                                    | Código: `200`     | El código de respuesta es `200 OK`                |
| 4  | Analizar el cuerpo de la respuesta (JSON)                                             | JSON de respuesta | La respuesta debe ser un objeto JSON válido       |
| 5  | Validar que el campo `id` esté presente y sea `171`                                   | Campo: `id`       | `id` está presente y su valor es `171`            |
| 6  | Validar que el campo `name` esté presente                                             | Campo: `name`     | El campo `name` existe en el JSON                 |
| 7  | Validar que el campo `status` esté presente                                           | Campo: `status`   | El campo `status` existe en el JSON               |
| 8  | Validar que el campo `species` esté presente                                          | Campo: `species`  | El campo `species` existe en el JSON              |

Resultado esperado:
La API devuelve código 200 OK.
El JSON incluye los campos: id, name, status, species.
El campo id debe tener valor 171.
"""
