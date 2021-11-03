import requests
import os
from dotenv import load_dotenv
from fetch_image import get_comics, fetch_comics


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


def upload_image(upload_url, image_name):
    with open(image_name, 'rb') as file:
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
    for spec in response.json()['response']:
        return spec['id'], spec['owner_id']


def post_comics(access_token, group_id, media_id, owner_id, comment):
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'access_token': access_token,
        'v': 5.131,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachment': f'photo{owner_id}_{media_id}',
        'message': comment,

    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    return response


load_dotenv()
client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('ACCESS_TOKEN')
group_id = os.getenv('GROUP_ID')
url, comment = get_comics()
image_name = fetch_comics(url)
# get_access_url(client_id)
# check_access_url(access_token)
upload_url = get_upload_url(access_token, group_id)
vk_hash, vk_photo, vk_server = upload_image(upload_url, image_name)
media_id, owner_id = save_image(access_token, group_id, vk_server, vk_hash, vk_photo)
response = post_comics(access_token, group_id, media_id, owner_id, comment)
if response:
    os.remove(image_name)







