import requests


class SyliusRequest:
    @staticmethod
    def get(url, headers):
        response = requests.get(url, headers=headers)
        return response

    @staticmethod
    def post(url, headers=None, payload=None):
        if headers is None:
            headers = {}
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        response = requests.post(url, headers=headers, json=payload)
        return response

    @staticmethod
    def put(url, headers, payload=None):
        headers = headers.copy()
        lower_keys = {k.lower() for k in headers.keys()}
        if 'content-type' not in lower_keys:
            headers['Content-Type'] = 'application/json'
        response = requests.put(url, headers=headers, json=payload)
        return response

    @staticmethod
    def put_with_custom_headers(url, headers, payload=None):
        headers = headers.copy()
        headers.update({'Content-Type': 'application/ld+json'})
        response = requests.put(url, headers=headers, json=payload)
        return response

    @staticmethod
    def delete(url, headers, payload=None):
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        response = requests.delete(url, headers=headers, json=payload)
        return response
