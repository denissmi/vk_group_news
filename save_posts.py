import argparse
import getpass
import logging
import vk_api


def setup_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    logger.addHandler(stream_handler)

    return logger


def parse_argument():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--login', dest='login', help='VK login')
    parser.add_argument('--group-name', dest='group_name', help='Name of the group of specified user')

    return parser.parse_args()


def main():
    logger = setup_logging()
    args = parse_argument()

    password = getpass.getpass()
    vk_session = vk_api.VkApi(args.login, password)
    vk_session.auth()

    vk = vk_session.get_api()
    user_groups = {item['name']: item for item in vk.groups.get(extended=True)['items']}
    group = user_groups.get(args.group_name)
    if not group:
        logger.warning(f'The specified group "{args.group_name}" not found in the list of your groups')
        return None

    return None


if __name__ == '__main__':
    main()
