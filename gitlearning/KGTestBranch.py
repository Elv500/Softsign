import requests

url = "https://rickandmortyapi.com/api/character/171"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)