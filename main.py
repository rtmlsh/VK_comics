import requests
import pprint
import os
from urllib.parse import urlparse


def get_comics():
    url = 'https://xkcd.com/353/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_comics(url):
    response = requests.get(url)
    path = urlparse(url)
    image_name = os.path.split(path.path)[-1]
    with open(image_name, 'wb') as file:
        file.write(response.content)


url = get_comics()['img']
print(get_comics()['alt'])
fetch_comics(url)



