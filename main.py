import argparse
import os
from urllib.parse import urlparse

from dotenv import load_dotenv

from fetch_comics import fetch_comics, get_comics, get_rand_comics_num
from post_comics import check_response

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скрипт интегрируется с API VK и xkcd, '
                    'и публикует комиксы на стене вк-сообщества'

    )

    load_dotenv()
    access_token = os.getenv('VK_ACCESS_TOKEN')
    group_id = os.getenv('GROUP_ID')
    client_id = os.getenv('CLIENT_ID')

    comics_num = get_rand_comics_num()
    url, title = get_comics(comics_num)

    path = urlparse(url)
    comics = os.path.split(path.path)[-1]

    fetch_comics(comics, url)

    try:
        check_response(access_token, group_id, title, comics)
    finally:
        os.remove(comics)