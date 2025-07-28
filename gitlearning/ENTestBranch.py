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
