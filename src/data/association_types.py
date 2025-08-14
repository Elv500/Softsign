from faker import Faker

fake = Faker()


def generate_association_types_source_data(code=None, en_US_name=None, include_es_ES=False, include_es_MX=False):
    code = code or fake.unique.bothify(text="??????????????????????????????????????")
    en_US_name = en_US_name or fake.word()

    data = {
        "code": code,
        "translations": {
            "en_US": {
                "name": en_US_name
            }
        }
    }
    if include_es_ES:
        data["translations"]["es_ES"] = {
            "name": fake.word()
        }
    if include_es_MX:
        data["translations"]["es_MX"] = {
            "name": fake.word()
        }
    return data


def generate_association_type_translations_data(langs=None, overrides=None, extra_fields=None):
    langs = langs or ["en_US"]
    overrides = overrides or {}
    extra_fields = extra_fields or {}

    translations = {}

    for lang in langs:
        lang_data = overrides.get(lang, {})
        if "name" in lang_data:
            name = lang_data["name"]
        else:
            name = fake.word()
        translations[lang] = {
            **({"@id": lang_data.get("@id")} if "@id" in lang_data else {}),
            "name": name
        }

    payload = {"translations": translations}
    payload.update(extra_fields)
    return payload


def build_auth_headers(headers=None, accept=True, content_type=True):
    headers = headers or {}
    if accept:
        headers["Accept"] = "application/ld+json"
    if content_type:
        headers["Content-Type"] = "application/ld+json"
    return headers
