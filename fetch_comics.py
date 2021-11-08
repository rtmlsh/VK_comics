import os
import random
from urllib.parse import urlparse

import requests


def get_comics_num():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return random.randint(0, response.json()['num'])


def get_comics(comics_num):
    url = f'https://xkcd.com/{comics_num}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    api_response = [response.json()['img'], response.json()['alt']]
    return api_response


def fetch_comics(url):
    response = requests.get(url)
    path = urlparse(url)
    comics = os.path.split(path.path)[-1]
    with open(comics, 'wb') as file:
        file.write(response.content)
    return comics
