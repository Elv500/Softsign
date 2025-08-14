# <!-- ID: TC-2
# Título: Validar el código 404 al hacer un request con un ID inexistente
# Descripción:
# El sistema debe retornar un código de estado HTTP 404 cuando el usuario realiza una petición GET para obtener un personaje que no existe en la base de datos.
# Llamada API:
# GET https://rickandmortyapi.com/api/character/999999
# Precondiciones
# El personaje con ID 999999 no debe existir en la aplicación.
# Tener acceso a internet y Postman instalado.
# Ambiente:
# URL base: https://rickandmortyapi.com
# Usuario: Acceso libre, no requiere autenticación
# Herramienta: Postman
# Pasos:
# Abrir Postman.
# Seleccionar método GET.
# Ingresar el endpoint:
# https://rickandmortyapi.com/api/character/999999
# Hacer clic en Send.

# Resultado esperado:
# El sistema debe retornar una respuesta HTTP 404 Not Found.
# El cuerpo de la respuesta debe incluir un mensaje de error como:

# {
#   "error": "Character not found"
# }
# Evidencias:
# .....

# Prioridad:Media
# Post Condition / Teardown:
# No aplica (el recurso es público y no se modifica). No es necesario borrar nada. -->




import requests
import pytest
# ID:TC_02
@pytest.mark.smoke
def test_TC_02_HTTP_status_code():
    """Descripcion: El usuario debe obtener la lista del obj. con id de 999999"""
    url = "https://rickandmortyapi.com/api/character/999999"
    response = requests.get(url)
    assert response.status_code == 404