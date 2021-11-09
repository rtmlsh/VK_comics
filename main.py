import argparse
import os

from dotenv import load_dotenv

from fetch_comics import get_comics_num, get_comics, fetch_comics
from post_comics import get_upload_url, upload_comics, save_comics, publish_comics


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
    comics = fetch_comics(url)

    upload_url = get_upload_url(access_token, group_id)
    hash_num, photo, server_num = upload_comics(upload_url, comics)
    media_id, owner_id = save_comics(
        access_token,
        group_id,
        server_num,
        hash_num,
        photo
    )
    response = publish_comics(
        access_token,
        group_id,
        media_id,
        owner_id,
        title
    )

    if response:
        os.remove(comics)
