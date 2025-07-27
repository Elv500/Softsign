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
