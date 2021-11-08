import argparse
import os

import requests
from dotenv import load_dotenv

from fetch_comics import get_comics_num, get_comics, fetch_comics
from post_comics import get_upload_url, upload_comics, save_comics, publish_comics


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
    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скрипт интегрируется с API VK и xkcd, '
                    'и публикует комиксы на стене вк-сообщества'

    )
    parser.add_argument(
        'client_id',
        help='Укажите client_id',
    )
    parser.add_argument(
        'group_id',
        help='Укажите group_id',
    )
    args = parser.parse_args()
    parser.parse_args()

    get_access_url(args.client_id)
    token = input('Введите access_token: ')
    if check_access_url(token):
        with open('.env', 'w') as file:
            file.write(f'VK_ACCESS_TOKEN={token}')

    load_dotenv()
    access_token = os.getenv('VK_ACCESS_TOKEN')

    comics_num = get_comics_num()
    url, title = get_comics(comics_num)
    comics = fetch_comics(url)

    upload_url = get_upload_url(access_token, args.group_id)
    hash_num, photo, server_num = upload_comics(upload_url, comics)
    media_id, owner_id = save_comics(
        access_token,
        args.group_id,
        server_num,
        hash_num,
        photo
    )
    response = publish_comics(
        access_token,
        args.group_id,
        media_id,
        owner_id,
        title
    )

    if response:
        os.remove(comics)
