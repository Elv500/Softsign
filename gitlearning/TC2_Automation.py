import pytest
import requests

#Titulo: Verificar que no se muestren los datos de objetos que no existen
#Descripcion: No se debe mostrar los datos de un objeto que no existe
#Pasos:
#1. Ingresar a Postman
#2. Seleccionar GET
#3. Copiar la URL: https://collectionapi.metmuseum.org/public/collection/v1/objects/123654
#4. Clic en Send
#5. Verificar la respuesta
#Metodo GET
#URL: https://collectionapi.metmuseum.org/public/collection/v1/objects/123654
#Ambiente: https://metmuseum.github.io/
#Prioridad: Media
#Categoria: Smoke test, Negative test

@pytest.mark.smoke
@pytest.mark.negative
def test002_verificar_que_no_se_muestren_los_datos_de_objetos_que_no_existen():
    """Descripcion: No se debe mostrar los datos de un objeto que no existe"""

    """Ambiente"""
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/123654"

    response = requests.request("GET", url)
    """Verificar la respuesta"""
    assert response.status_code == 404



#Titulo: Verificar que no se pueda consultar datos con parametros incorrectos
#Descripcion: No se debe mostrar los datos de un objeto cuando se envia parametros incorrectos en la consulta
#Pasos:
#1. Ingresar a Postman
#2. Seleccionar GET
#3. Copiar la URL: https://collectionapi.metmuseum.org/public/collection/v1/objects/a
#4. Clic en Send
#5. Verificar la respuesta
#Metodo GET
#URL: https://collectionapi.metmuseum.org/public/collection/v1/objects/a
#Ambiente: https://metmuseum.github.io/
#Prioridad: Media
#Categoria: Smoke test, Negative test
def test003_verificar_que_no_se_pueda_consultar_datos_con_parametros_incorrectos():
    """Descripcion: No se debe mostrar los datos de un objeto cuando se envia parametros incorrectos en la consulta """

    """Ambiente"""
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/a"

    response = requests.request("GET", url)
    """Verificar la respuesta"""
    assert response.status_code == 400