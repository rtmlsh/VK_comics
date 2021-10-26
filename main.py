import requests


url = 'https://xkcd.com/353/info.0.json'
response = requests.get(url)
response.raise_for_status()
print(response.json())
