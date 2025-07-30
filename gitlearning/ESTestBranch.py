import requests

url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

payload = {}
headers = {
  'Cookie': 'incap_ses_1721_1662004=k7YbcxexCmr99YLevjjiF/cxgGgAAAAAYK6QT2XMqRUJ61WWdRqmCA==; incap_ses_1725_1662004=OKPfX+7EahkXu4Ict27wFxxhgGgAAAAA9N1h/24jD/8Epr+t0ypMWg==; visid_incap_1662004=JuAxQg5fQmGFbTkieVID1UMjgGgAAAAAQUIPAAAAAADxdTOzJWztFGe9SAt/nP3a'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)