import pytest
import requests
import json
import jsonschema


@pytest.mark.smoke
@pytest.mark.funcional
def test_003_adicionar_objetos():
    url = "https://api.restful-api.dev/objects"

    payload = json.dumps({
        "data": {
            "CPU model": "n_U0K.O\ta",
            "Hard disk size": "",
            "price": 1.4719386661760225,
            "year": 110740
        },
        "name": "Ou2\""
    })
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    assert response.status_code == 200

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "data",
            "name"
        ],
        "properties": {
            "name": {
                "type": "string"
            },
            "data": {
                "type": "object",
                "required": [
                    "CPU model",
                    "Hard disk size",
                    "price",
                    "year"
                ],
                "properties": {
                    "year": {
                        "type": "integer"
                    },
                    "price": {
                        "type": "number"
                    },
                    "CPU model": {
                        "type": "string"
                    },
                    "Hard disk size": {
                        "type": "string"
                    }
                }
            }
        }
    }

    try:
        jsonschema.validate(instance=response.json(), schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        pytest.fail(f"JSON schema doesn't match: {err}")
