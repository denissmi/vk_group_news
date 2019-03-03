import argparse
import base64
import getpass
import json
import logging
import urllib.parse
import urllib.request
import vk_api

from datetime import datetime
from pathlib import Path

from vk.settings import MEDIA_ROOT

MEDIA_ROOT = Path(MEDIA_ROOT)


def setup_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    logger.addHandler(stream_handler)

    return logger


class VkPost:
    def __init__(self, text, image, publication_date, message_id, link):
        self.text = text
        self.image = image
        self.publication_date = publication_date
        self.message_id = message_id
        self.link = link

    @classmethod
    def from_group(cls, login, password, group_name):
        logger = setup_logging()

        vk_session = vk_api.VkApi(login, password)
        vk_session.auth()

        vk = vk_session.get_api()
        user_groups = {item['name']: item for item in vk.groups.get(extended=True)['items']}
        group = user_groups.get(group_name)
        if not group:
            logger.warning(f'The specified group "{group_name}" not found in the list of your groups')
            return []

        group_wall = vk.wall.get(owner_id=group['id'], filter='owner')
        print(group_wall)
        vk_posts = []
        for item in group_wall['items']:
            publication_date = datetime.fromtimestamp(item['date'])
            message_id = f'{item["owner_id"]}_{item["id"]}'
            if not item['attachments']:
                vk_posts.append(cls(text=item['text'], image=None, publication_date=publication_date,
                                    message_id=message_id, link=None))
                continue

            for attachment in item['attachments']:
                if attachment['type'] != 'photo':
                    continue

                photo_data = attachment['photo']
                if not photo_data['sizes']:
                    continue

                photo_urls = {s['type']: s['url'] for s in photo_data['sizes']}
                biggest_photo_type = sorted(photo_urls.keys())[-1]
                biggest_photo_url = photo_urls[biggest_photo_type]
                parsed_url = urllib.parse.urlparse(biggest_photo_url)
                file_name = parsed_url.path.split('/')[-1]
                MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
                photo_path, _ = urllib.request.urlretrieve(biggest_photo_url, MEDIA_ROOT / file_name)
                with photo_path.open('rb') as image_file:
                    encoded_image = base64.b64encode(image_file.read())
                decoded_image = encoded_image.decode('utf-8')
                vk_posts.append(cls(text=item['text'], image=decoded_image, publication_date=publication_date,
                                    message_id=message_id, link=None))

        return vk_posts

    def as_dict(self):
        return {'text': self.text, 'image': self.image, 'publication_date': self.publication_date.isoformat(),
                'message_id': self.message_id, 'link': self.link}


class VkGroupNewsClient:
    api_address = 'http://localhost:8000'

    def __init__(self, api_address: str = None):
        self.api_address = api_address or self.api_address

    def _make_request(self, endpoint: str, data=None, headers=None, method=None):
        if data:
            data = json.dumps(data).encode('utf-8')
        headers = headers or {'Content-Type': 'application/json; charset=utf-8'}
        request = urllib.request.Request(f'{self.api_address}/{endpoint}/', data=data, headers=headers, method=method)
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read())

    def post(self, endpoint, data, headers=None):
        return self._make_request(endpoint, headers=headers, data=data, method='POST')


def parse_argument():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--login', dest='login', help='VK login')
    parser.add_argument('--group-name', dest='group_name', help='Name of the group of specified user')
    parser.add_argument('--api-address', dest='api_address', default=VkGroupNewsClient.api_address,
                        help='VK group news REST API address')
    return parser.parse_args()


def main():
    args = parse_argument()

    password = getpass.getpass()
    vk_posts = VkPost.from_group(args.login, password, args.group_name)
    vk_group_news_client = VkGroupNewsClient()
    for vk_post in vk_posts:
        vk_group_news_client.post('vk_posts', vk_post.as_dict())


if __name__ == '__main__':
    main()
