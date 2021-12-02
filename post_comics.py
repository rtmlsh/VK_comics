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
    try:
        return response.json()['response']['upload_url']
    except:
        check_errors(response)
        raise


def upload_comics(upload_url, comics):
    with open(comics, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    try:
        server_response = response.json()
        return \
            server_response['hash'],\
            server_response['photo'],\
            server_response['server']
    except Exception:
        check_errors(response)
        raise


def save_comics(access_token, group_id, server_num, hash_num, photo):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': access_token,
        'group_id': group_id,
        'v': 5.131,
        'server': server_num,
        'hash': hash_num,
        'photo': photo,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    try:
        specs = response.json()['response'][0]
        return specs['id'], specs['owner_id']
    except Exception:
        check_errors(response)
        raise


def publish_comics(access_token, group_id, media_id, owner_id, title):
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'access_token': access_token,
        'v': 5.131,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachment': f'photo{owner_id}_{media_id}',
        'message': title,

    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    try:
        return response
    except Exception:
        check_errors()
        raise


def check_errors(response):
    error = response.json()['error']
    if error:
        print(
             f"Error: {error['error']['error_msg']}"
         )
