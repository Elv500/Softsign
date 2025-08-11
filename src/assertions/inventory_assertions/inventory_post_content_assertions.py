import pytest

class AssertionInventoryCreate:

    @staticmethod
    def assert_inventory_payload(payload, required_only=False):
        try:
            assert payload["code"] != "", "Campo 'code' vacio"
            assert payload["name"] != "", "Campo 'name' vacio"

            if not required_only:
                assert all(campo.strip() != "" for campo in payload["address"].values()), "Campo 'address' vacio"
                assert payload["priority"] >= 0, "Campo 'priority' vacio"
                assert len(payload["channels"]) >= 0, "Campo 'channel' longitud invalido"
                assert all(channel.strip() != "" for channel in payload["channels"]), "Campo dentro de 'channel' vacio"
            
        except AssertionError as e:
            pytest.fail(f"Error en el payload: {e}")

    @staticmethod
    def assert_inventory_response(payload, response_json, required_only=False):
        try:
            assert response_json["@context"].strip() != "", "Campo '@context' está vacío"
            assert response_json["@id"].strip() != "", "Campo '@id' está vacío"
            assert response_json["@type"].strip() != "", "Campo '@type' está vacío"
            
            #Implementar si se agrega en el Scope la funcion Addres (Client)
            #assert response_json["address"] == payload["address"]
            
            assert response_json["id"] >= 0
            assert response_json["code"] == payload["code"]
            assert response_json["name"] == payload["name"]
            if required_only:
                assert response_json["priority"] == 0
                assert response_json["channels"] == []
            else:
                assert response_json["priority"] == payload["priority"]
                assert response_json["channels"] == payload["channels"]

        except AssertionError as e:
            pytest.fail(f"Error en el response: {e}")