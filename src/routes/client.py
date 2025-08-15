# import http.client
# from urllib.parse import urlparse
# import json

# class SyliusClient:
#     @staticmethod
#     def get(full_url, headers):
#         partes = urlparse(full_url)
#         path = partes.path
#         if partes.query:
#             path += "?" + partes.query

#         conn = http.client.HTTPSConnection(partes.netloc)
#         conn.request("GET", path, headers=headers)
#         res = conn.getresponse()

#         class ResponseLike:
#             def __init__(self, res):
#                 self.status = res.status
#                 self.status_code = res.status
#                 self.content = res.read()
#             def json(self):
#                 return json.loads(self.content.decode())

#         return ResponseLike(res)