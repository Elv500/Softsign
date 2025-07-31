import requests

url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

payload = {}
headers = {
  'Cookie': 'incap_ses_765_1662004=1Y8kHE6w7kgh1SRDuNOdCuIrgGgAAAAAxkFuEyMDRo45XHl1UWViCw==; visid_incap_1662004=D1lT+uRCSqimcrQduDOSugIjgGgAAAAAQUIPAAAAAABffnttKv+gD5ASya8GrXIm'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)