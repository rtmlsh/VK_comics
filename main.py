import requests
import os
from dotenv import load_dotenv
from fetch_image import get_comics, fetch_comics
from post_comics import get_upload_url, upload_image, save_image, post_comics


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


if __name__ == '__main__':
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







