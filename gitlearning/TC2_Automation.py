import requests
import pytest

def test_get_character_not_found():

    url = "https://rickandmortyapi.com/api/character/999999"
    response = requests.get(url)

    assert response.status_code == 404, f"Se esperaba código 404 pero se obtuvo {response.status_code}"

    error_data = response.json()
    assert "error" in error_data, "La respuesta de error no contiene el campo 'error'"

"""
Test Case: API > Get Character – Buscar personaje inexistente
Descripción:
Verifica que al realizar una solicitud GET con un ID de personaje que no existe (999999), la API de Rick and Morty retorne un código de estado 404 junto con un mensaje de error que incluya el campo "error" en el cuerpo de la respuesta.

Precondiciones:

Tener Postman o entorno Python configurado con requests y pytest.

Conexión activa a Internet.

La API debe estar disponible en línea.

Prioridad: Alta

Tipo de prueba: Funcional – Negativa

Datos de prueba:

URL: https://rickandmortyapi.com/api/character/999999

Método: GET
| N° | Paso                                                                                    | Entrada           | Resultado Esperado                                            |
| -- | --------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------- |
| 1  | Abrir Postman o ejecutar el script en Python                                            | N/A               | La herramienta está lista para ejecutar la solicitud          |
| 2  | Enviar una solicitud GET al endpoint `https://rickandmortyapi.com/api/character/999999` | Método: `GET`     | Se recibe una respuesta de la API                             |
| 3  | Verificar el código de estado HTTP                                                      | Código: `404`     | La respuesta es `404 Not Found`                               |
| 4  | Analizar el cuerpo de la respuesta                                                      | JSON de respuesta | La respuesta es un JSON con un campo `error`                  |
| 5  | Verificar que el campo `"error"` exista en la respuesta                                 | Clave: `error`    | El campo `"error"` está presente en el cuerpo de la respuesta |

Resultado esperado:
El código de respuesta HTTP es 404 Not Found.

La respuesta contiene un JSON con un campo "error" que indica que el recurso no fue encontrado.
"""







def test_method_not_allowed():
    url = "https://rickandmortyapi.com/api/character/171"

    response = requests.post(url, data={})

    assert response.status_code == 405, f"Se esperaba código 405 pero se obtuvo {response.status_code}"
    assert 'Allow' in response.headers, "El header Allow no está presente"
    assert 'GET' in response.headers['Allow'], "GET debería estar en los métodos permitidos"



    def test_bad_request_invalid_id_format():

        url = "https://rickandmortyapi.com/api/character/invalid_id"
        response = requests.get(url)

        assert response.status_code == 400, f"Se esperaba código 400 pero se obtuvo {response.status_code}"

        error_data = response.json()
        assert "error" in error_data, "La respuesta de error debería contener un campo 'error'"