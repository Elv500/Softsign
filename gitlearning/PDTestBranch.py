import requests

url = "https://reqres.in/api/users?page=1"

payload = {}
headers = {
  'x-api-key': 'reqres-free-v1'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)