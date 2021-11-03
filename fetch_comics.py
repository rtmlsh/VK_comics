import os
import random
from urllib.parse import urlparse

import requests


def get_rand_num():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return random.randint(0, response.json()['num'])


def get_comics():
    random_num = get_rand_num()
    url = f'https://xkcd.com/{random_num}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['img'], response.json()['alt']


def fetch_comics(url):
    response = requests.get(url)
    path = urlparse(url)
    image_name = os.path.split(path.path)[-1]
    with open(image_name, 'wb') as file:
        file.write(response.content)
    return image_name
