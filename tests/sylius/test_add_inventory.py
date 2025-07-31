import requests
import json
import pytest
import jsonschema

def test_add_inventory():

    url = "https://demo.sylius.com/api/v2/admin/inventory-sources"

    payload = json.dumps({
    "address": {
        "countryCode": "US",
        "street": "string",
        "city": "string",
        "postcode": "string"
    },
    "code": "pruebaEAs",
    "name": "string",
    "priority": 0,
    "channels": [
        "/api/v2/admin/channels/HOME_WEB"
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTM4MzMxMDksImV4cCI6MTc1MzgzNjcwOSwicm9sZXMiOlsiUk9MRV9BRE1JTklTVFJBVElPTl9BQ0NFU1MiLCJST0xFX0FQSV9BQ0NFU1MiXSwidXNlcm5hbWUiOiJhcGkifQ.AvSzOFZUyr5OPLwDtSOMYiUpzAy_iGeU9yrYaV355Sycw8QkcsXhFhSHEnav6lSx_BTDZu3LKsqZyKC6kIwsxpNmnmo385wuKBUoh7jnSo1LQr4NZcFzAocqrs0sUrktWgNNXX92yZ2jEnuVCF02OGyfi29Kgjl3WpYRhczUF6lJJNnexqylUcjDmC7VrSkWi1_IZAoSEqSkrWuRgEzJlHVk8VdvgUB8DjacDHN8aIyHSB4-fiLNUC8KWYH5DXB-awA0G8brahLO_ze9diD0SE88NV_48QFHPACt-WjsJJPoNwSo6IEHg_v_w1QSEyDTyFSlKeeRi1jZgsJjxhYlB3IHcD9i_wrSYr0IZxHKbYP9TBf7h9kYZiOgQyRwcO1vbP0nTRbXTRtJulhEVxER67xTzQ2hKYTiA2PpPxWBhpvXZGKV_-Q8KQWKWTbU41_0SLJ-GLQdfQ8DLbh-yB31flqn5jkPlS4lPQM9da1SG7NIv42DASo-AoYdbKnmKYRBhadx05pCI29qRqQKg_kzw9mSFFlpxvT-lN8p-pMdoSMKVuGmpEPbQNpJu83fxMWlxGAZr82mo-xxUbUrAvI4DUhUoT4yqEyvMhdiGlroXcKoX_gBdUQTZ349gaSf6kJtGoikzEjBCFKIa0PD__dvOI8s7ss6gJCM-pcir5RsYWc'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    assert response.status_code == 201

    schema = {
            "type": "object",
            "required": [
                "@context",
                "@id",
                "@type",
                "address",
                "channels",
                "code",
                "id",
                "name",
                "priority"
            ],
            "properties": {
                "@context": {
                    "type": "string"
                },
                "@id": {
                    "type": "string"
                },
                "@type": {
                    "type": "string"
                },
                "id": {
                    "type": "integer"
                },
                "address": {
                    "type": "string"
                },
                "code": {
                    "type": "string"
                },
                "name": {
                    "type": "string"
                },
                "priority": {
                    "type": "integer"
                },
                "channels": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
    try:
        jsonschema.validate(instance=response.json(), schema=schema)

    except jsonschema.exceptions.ValidationError as err:
        pytest.fail(f"JSON schema doesnt match {err}")