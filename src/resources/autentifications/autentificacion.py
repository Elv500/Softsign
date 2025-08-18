from utils.load_resources import load_credential_resource

class Auth:
    def __init__(self):
        self.users = self.load_file()

    @staticmethod
    def load_file():
        return load_credential_resource("credentials_admin.json")

    def get_credential(self, tipo):
        return self.users.get(tipo)

    def build_payload(self, tipo, adicionales=None):
        cred = self.get_credential(tipo)
        payload = {"email": cred["email"], "password": cred["password"]}
        if adicionales:
            payload.update(adicionales)
        return payload

    def get_valid_login_payload(self, adicionales=None):
        return self.build_payload("valid_credential", adicionales)

    def get_invalid_login_payload(self, adicionales=None):
        return self.build_payload("invalid_credential", adicionales)

    def get_invalid_email_payload(self, adicionales=None):
        return self.build_payload("invalid_email_credential", adicionales)

    def get_invalid_password_payload(self, adicionales=None):
        return self.build_payload("invalid_password_credential", adicionales)

    def get_empty_credential_payload(self, adicionales=None):
        return self.build_payload("empty_credential", adicionales)

    def get_empty_email_payload(self, adicionales=None):
        return self.build_payload("empty_email_credential", adicionales)

    def get_empty_password_payload(self, adicionales=None):
        return self.build_payload("empty_password_credential", adicionales)