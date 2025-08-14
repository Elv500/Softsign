import requests

from utils.logger_helpers import log_request_response


class SyliusRequest:
    @staticmethod
    def get(url, headers):
        response = requests.get(url, headers=headers)
        log_request_response(url, response, headers)
        return response

    @staticmethod
    def post(url, headers=None, payload=None):
        if headers is None:
            headers = {}
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        response = requests.post(url, headers=headers, json=payload)
        log_request_response(url, response, headers, payload)
        return response

    @staticmethod
    def put(url, headers, payload=None):
        headers = headers.copy()
        lower_keys = {k.lower() for k in headers.keys()}
        if 'content-type' not in lower_keys:
            headers['Content-Type'] = 'application/json'
        response = requests.put(url, headers=headers, json=payload)
        log_request_response(url, response, headers, payload)
        return response

    @staticmethod
    def delete(url, headers, payload=None):
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        response = requests.delete(url, headers=headers, json=payload)
        log_request_response(url, response, headers, payload)
        return response
