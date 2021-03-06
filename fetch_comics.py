import random

import requests


def get_rand_comics_num():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return random.randint(0, response.json()['num'])


def get_comics(comics_num):
    url = f'https://xkcd.com/{comics_num}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    api_response = response.json()
    return api_response['img'], api_response['alt']


def fetch_comics(comics, url):
    response = requests.get(url)
    response.raise_for_status()
    with open(comics, 'wb') as file:
        file.write(response.content)

