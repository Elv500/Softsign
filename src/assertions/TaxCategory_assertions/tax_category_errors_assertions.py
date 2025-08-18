class AssertionTaxCategoryErrors:
    """Assertions para errores de Tax Category en Sylius API."""

    # ----------- Métodos generales de respuesta -----------

    @staticmethod
    def assert_tax_category_errors(response_json, status_code_expected, message_expected):
        """Valida status y mensaje genérico de error en Tax Category."""
        AssertionTaxCategoryErrors._assert_status_code(response_json, status_code_expected)
        AssertionTaxCategoryErrors._assert_message_contains(response_json, message_expected)

    @staticmethod
    def assert_invalid_token_error(response_json):
        """Valida que el error sea por token inválido."""
        msg = response_json.get("message", "").lower()
        valids = ["jwt token not found", "invalid jwt token", "invalid credentials."]
        assert msg in valids, f"Mensaje inesperado para token inválido: {msg}"

    @staticmethod
    def assert_not_found_error(response_json, status_code_expected=404, message_expected="Not Found"):
        """Valida error 404 y mensaje de recurso no encontrado."""
        AssertionTaxCategoryErrors._assert_status_code(response_json, status_code_expected)
        msg = AssertionTaxCategoryErrors._get_full_message(response_json)
        assert message_expected.lower() in msg or "not found" in msg or "no encontrado" in msg, \
            f"El mensaje no indica recurso no encontrado. Mensaje: {msg}"

    # ----------- Métodos de errores de campos -----------

    @staticmethod
    def assert_duplicate_code_error(response_json):
        """Valida error de código duplicado."""
        violations = AssertionTaxCategoryErrors._get_violations(response_json)
        AssertionTaxCategoryErrors._assert_violation_field(violations, "code")
        assert any("ya existe" in v["message"].lower() or "exists" in v["message"].lower() for v in violations), \
            f"El mensaje de error no indica duplicado. Violations: {violations}"

    @staticmethod
    def assert_missing_field_error(response_json, field_name):
        """Valida error de campo obligatorio faltante."""
        violations = AssertionTaxCategoryErrors._get_violations(response_json)
        AssertionTaxCategoryErrors._assert_violation_field(violations, field_name)
        assert any(
            "please enter" in v["message"].lower() or "cannot be blank" in v["message"].lower()
            for v in violations
        ), f"El mensaje de error no indica que '{field_name}' es obligatorio. Violations: {violations}"

    @staticmethod
    def assert_max_length_error(response_json, field_name):
        """Valida error de longitud máxima excedida."""
        violations = AssertionTaxCategoryErrors._get_violations(response_json)
        AssertionTaxCategoryErrors._assert_violation_field(violations, field_name)
        assert any(
            "must not be longer than" in v["message"].lower() for v in violations
        ), f"El mensaje de error no indica que '{field_name}' excede longitud máxima. Violations: {violations}"

    @staticmethod
    def assert_min_length_error(response_json, field_name):
        """Valida error de longitud mínima no alcanzada."""
        violations = AssertionTaxCategoryErrors._get_violations(response_json)
        AssertionTaxCategoryErrors._assert_violation_field(violations, field_name)
        assert any(
            "least" in v["message"].lower() and "characters" in v["message"].lower()
            for v in violations
        ), f"El mensaje de error no indica que '{field_name}' no cumple longitud mínima. Violations: {violations}"

    # ----------- Métodos auxiliares privados -----------

    @staticmethod
    def _get_full_message(response_json):
        """Concatena los mensajes posibles en la respuesta."""
        return (
            response_json.get("message", "") +
            response_json.get("detail", "") +
            response_json.get("description", "")
        ).lower()

    @staticmethod
    def _assert_status_code(response_json, expected):
        """Valida el status code en la respuesta."""
        assert response_json.get("status", expected) == expected, \
            f"El status recibido no es {expected}: {response_json.get('status')}"

    @staticmethod
    def _get_violations(response_json):
        """Obtiene la lista de violations."""
        assert "violations" in response_json, "No se encontró la clave 'violations' en la respuesta."
        return response_json["violations"]

    @staticmethod
    def _assert_violation_field(violations, field_name):
        """Valida que haya error para el campo esperado."""
        assert any(v["propertyPath"] == field_name for v in violations), \
            f"No se encontró error asociado al campo '{field_name}'. Violations: {violations}"

    @staticmethod
    def _assert_message_contains(response_json, expected_message):
        """Valida que el mensaje contenga el texto esperado."""
        msg = AssertionTaxCategoryErrors._get_full_message(response_json)
        assert expected_message.lower() in msg, \
            f"El mensaje no indica error esperado. Mensaje: {msg}"

