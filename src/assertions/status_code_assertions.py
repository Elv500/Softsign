import pytest


class AssertionStatusCode:
    @staticmethod
    def assert_status_code(response, expected_status_code):
        assert response.status_code == expected_status_code

    @staticmethod
    def assert_status_code_200(response):
        assert response.status_code == 200

    @staticmethod
    def assert_status_code_201(response):
        assert response.status_code == 201
        
    @staticmethod
    def assert_status_code_204(response):
        assert response.status_code == 204

    @staticmethod
    def assert_status_code_400(response):
        assert response.status_code == 400

    @staticmethod
    def assert_status_code_401(response):
        assert response.status_code == 401

    @staticmethod
    def assert_status_code_403(response):
        assert response.status_code == 403

    @staticmethod
    def assert_status_code_404(response):
        assert response.status_code == 404

    @staticmethod
    def assert_status_code_405(response):
        assert response.status_code == 405

    @staticmethod
    def assert_status_code_409(response):
        assert response.status_code == 409
        
    @staticmethod
    def assert_status_code_415(response):
        assert response.status_code == 415

    @staticmethod
    def assert_status_code_422(response):
        assert response.status_code == 422

    @staticmethod
    def assert_status_code_500(response):
        assert response.status_code == 500

    @staticmethod
    def assert_status_code_422(response):
        assert response.status_code == 422
