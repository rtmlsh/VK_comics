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
        'scope': 'photos,groups,wall,offline',
        'response_type': 'token'
    }
    response = requests.get(vk_url, params=payload)
    print(response.url)


def check_access_url(access_token):
    vk_api_url = 'https://api.vk.com/method/groups.get'
    payload = {
        'access_token': access_token,
        'v': 5.131,
        'extended': 1,
    }
    response = requests.get(vk_api_url, params=payload)
    response.raise_for_status()
    pprint.pprint(response.json())


def get_upload_url(access_token, group_id):
    vk_api_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
            'access_token': access_token,
            'group_id': group_id,
            'v': 5.131
        }
    response = requests.get(vk_api_url, params=payload)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_image(upload_url):
    with open('python.png', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        return response.json()['hash'], response.json()['photo'], response.json()['server']


def save_image(access_token, group_id, vk_server, vk_hash, vk_photo):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': access_token,
        'group_id': group_id,
        'v': 5.131,
        'server': vk_server,
        'hash': vk_hash,
        'photo': vk_photo,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    pprint.pprint(response.json())



load_dotenv()
client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('ACCESS_TOKEN')
group_id = os.getenv('GROUP_ID')
# get_access_url(client_id)
# check_access_url(access_token)
upload_url = get_upload_url(access_token, group_id)
vk_hash, vk_photo, vk_server = upload_image(upload_url)
save_image(access_token, group_id, vk_server, vk_hash, vk_photo)

# url = get_comics()['img']
# print(get_comics()['alt'])
# fetch_comics(url)




