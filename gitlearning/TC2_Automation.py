import pytest
import requests

"""
Título
- Verificar que no se obtengan datos de un libro inexistente
Descripción
- El usuario no debe obtener los datos de un libro específico si su ID no existe
Precondiciones
- MÉTODO: GET
- URL: https://restful-booker.herokuapp.com/booking/1
Ambiente
- Acceso a API Doc: https://restful-booker.herokuapp.com/apidoc/
Prioridad
- Media
Categoría
- Negative / Smoke
"""

@pytest.mark.smoke
@pytest.mark.negative
def test002_verificar_que_no_se_obtengan_datos_de_un_libro_inexistente():
    """Descripción: El usuario no debe obtener los datos de un libro que no existe en el sistema"""
    
    # Ambiente
    url = "https://restful-booker.herokuapp.com/booking/1"
    
    response = requests.get(url)
    
    # Verificación
    assert response.status_code == 404