import requests

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