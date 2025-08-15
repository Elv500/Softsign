import http.client
import json
from urllib.parse import urlparse


def construir_path(url):
    partes = urlparse(url)
    host = partes.netloc
    path = partes.path
    if partes.query:
        path += "?" + partes.query
    return host, path


class ResponseLike:
    def __init__(self, res):
        self.status = res.status
        self.status_code = res.status
        self.content = res.read()
        self.text = self.content.decode(errors="ignore")

    def json(self):
        return json.loads(self.content.decode())


class SyliusClient:
    @staticmethod
    def get(url, headers):
        host, path = construir_path(url)
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        return ResponseLike(res)

    @staticmethod
    def post(url, headers=None, payload=None):
        host, path = construir_path(url)
        conn = http.client.HTTPSConnection(host)
        if headers is None:
            headers = {}
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        body = json.dumps(payload) if payload else None
        conn.request("POST", path, body, headers)
        res = conn.getresponse()
        return ResponseLike(res)

    @staticmethod
    def put(url, headers=None, payload=None):
        host, path = construir_path(url)
        conn = http.client.HTTPSConnection(host)
        headers = headers.copy() if headers else {}
        lower_keys = {k.lower() for k in headers.keys()}
        if 'content-type' not in lower_keys:
            headers['Content-Type'] = 'application/json'
        body = json.dumps(payload or {})
        conn.request("PUT", path, body, headers)
        res = conn.getresponse()
        return ResponseLike(res)

    @staticmethod
    def put_with_custom_headers(url, headers=None, payload=None):
        host, path = construir_path(url)
        conn = http.client.HTTPSConnection(host)
        headers = headers.copy() if headers else {}
        headers.update({'Content-Type': 'application/ld+json'})
        body = json.dumps(payload or {})
        conn.request("PUT", path, body, headers)
        res = conn.getresponse()
        return ResponseLike(res)

    @staticmethod
    def delete(url, headers=None, payload=None):
        host, path = construir_path(url)
        conn = http.client.HTTPSConnection(host)
        headers = headers.copy() if headers else {}
        headers.update({'Content-Type': 'application/json'})
        body = json.dumps(payload or {})
        conn.request("DELETE", path, body, headers)
        res = conn.getresponse()
        return ResponseLike(res)