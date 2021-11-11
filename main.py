import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

from fetch_comics import fetch_comics, get_comics, get_comics_num
from post_comics import (get_upload_url, publish_comics, save_comics,
                         upload_comics)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скрипт интегрируется с API VK и xkcd, '
                    'и публикует комиксы на стене вк-сообщества'

    )

    load_dotenv()
    access_token = os.getenv('VK_ACCESS_TOKEN')
    group_id = os.getenv('GROUP_ID')
    client_id = os.getenv('CLIENT_ID')

    comics_num = get_comics_num()
    url, title = get_comics(comics_num)

    path = urlparse(url)
    comics = os.path.split(path.path)[-1]

    try:
        fetch_comics(comics, url)
        upload_url = get_upload_url(access_token, group_id)
        hash_num, photo, server_num = upload_comics(upload_url, comics)
        media_id, owner_id = save_comics(
            access_token,
            group_id,
            server_num,
            hash_num,
            photo
        )
        try:
            response = publish_comics(
                access_token,
                group_id,
                media_id,
                owner_id,
                title
            )
        except (requests.HTTPError, requests.ConnectionError,
                requests.TooManyRedirects) as error:
            print(error, response.text)

    finally:
        os.remove(comics)