import requests
import pprint
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


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


def get_access_url(client_id):
    vk_url = 'https://oauth.vk.com/authorize'
    payload = {
        'client_id': client_id,
        'scope': 'photos, groups',
        'response_type': 'token'
    }
    response = requests.get(vk_url, params=payload)
    return response.url

url = get_comics()['img']
print(get_comics()['alt'])
fetch_comics(url)


load_dotenv()
client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('ACCESS_TOKEN')
user_id = os.getenv('USER_ID')




vk_api_url = 'https://api.vk.com/method/groups.get'
payload = {
        'access_token': access_token,
        'extended': 1,
        'v': 5.131
    }
response = requests.get(vk_api_url, params=payload)
response.raise_for_status()
pprint.pprint(response.json())



