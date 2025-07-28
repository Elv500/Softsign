
import requests
import json

url = "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers"

payload = json.dumps({
  "name": "Fernando MacBook Pro 16",
  "data": {
    "year": 2025,
    "price": 1849.99,
    "CPU model": "Intel Core i9",
    "Hard disk size": "1 TB"
  }
})
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'orangehrm=pulbmrjh4vitabas9uo5snfd62'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
