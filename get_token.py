import argparse

import requests


def get_access_url(client_id):
    vk_url = 'https://oauth.vk.com/authorize'
    payload = {
        'client_id': client_id,
        'scope': 'photos,groups,wall,offline',
        'response_type': 'token'
    }
    response = requests.get(vk_url, params=payload)
    return response.url


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
        description='Скрипт интегрируется с API VK'
                    'для получения токена доступа'
    )

    parser.add_argument(
        'client_id',
        help='Укажите client_id',
    )

    args = parser.parse_args()
    parser.parse_args()

    print(get_access_url(args.client_id))

    token = input('Проверьте access_token: ')
    if check_access_url(token):
        print('Токен работает')
