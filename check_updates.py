import time

import requests
import sys
import logging
from logging.handlers import RotatingFileHandler
from bs4 import BeautifulSoup


class Kijiji:
    def __init__(self):
        self.urls = None

    def get_urls(self):
        try:
            with open('links.txt') as f:
                urls = f.read().strip().split('\n')
                self.urls = {url: [] for url in urls}
        except Exception as e:
            logger.error(f'could not read urls from links.txt [{" ".join(str(e).split())}]')

    def search(self, url):
        try:
            start_time = time.time()
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/85.0.4183.102 Safari/537.36',
            })
            # TODO: get the titles from search result and return titles
            soup = BeautifulSoup(response.content, 'html.parser')
            try:
                title_tags = soup.find_all('a', {'class': 'title'})
                titles = []
                for title_tag in title_tags:
                    try:
                        titles.append(title_tag.text.strip())
                    except:
                        pass
                logger.info(f'{url}: {len(titles)} results found in {round(time.time() - start_time, 2)} seconds')
                return titles
            except Exception as e:
                logger.error(f'could not get search results. [{error_str(e)}]')
                return []

        except Exception as e:
            print(e)

    def compare_search_results(self, url):
        pass


def error_str(err):
    return ' '.join(str(err).split())


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

    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('bs4').setLevel(logging.WARNING)
    logger = logging.getLogger()

    kijiji = Kijiji()
    kijiji.get_urls()
    for url in kijiji.urls:
        titles = kijiji.search(url)
        # print(titles)
        # print('-' * 100)
