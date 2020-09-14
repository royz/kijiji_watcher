import requests
import sys
import logging
from logging.handlers import RotatingFileHandler


class Kijiji:
    def __init__(self):
        self.urls = None

    def search(self, url):
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/85.0.4183.102 Safari/537.36',
            })
        except Exception as e:
            print(e)

    def get_urls(self):
        try:
            with open('links.txt') as f:
                self.urls = f.read().strip().split('\n')
        except Exception as e:
            logger.error(f'could not read urls from links.txt [{" ".join(str(e).split())}]')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=(
            RotatingFileHandler(
                filename='kijiji.log',
                maxBytes=(1024 ** 3) / 2,  # max log file size 512MB
                backupCount=1,
            ),
            logging.StreamHandler(sys.stdout)
        )
    )
    logger = logging.getLogger()
