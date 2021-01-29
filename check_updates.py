import time
import os
import requests
import sys
import logging
from logging.handlers import RotatingFileHandler
from bs4 import BeautifulSoup
import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(__file__)


class Kijiji:
    def __init__(self):
        self.urls = None
        self.notified_results = []
        self.get_urls()

    def get_urls(self):
        filename = os.path.join(BASE_DIR, f'links{input_id}.txt')
        try:
            with open(filename, encoding='utf-8') as f:
                urls = f.read().strip().split('\n')
                self.urls = {url: [] for url in urls}
        except Exception as e:
            logger.error(f'could not read urls from links.txt [{" ".join(str(e).split())}]')
            return []

    @staticmethod
    def search(url):
        try:
            start_time = time.time()
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/85.0.4183.102 Safari/537.36',
            })

            results = []
            soup = BeautifulSoup(response.content, 'html.parser')
            try:
                search_results = soup.find_all('div', {'class': 'search-item'})
            except Exception as e:
                logger.error(f'could not get search results. [{error_str(e)}]')
                return []
            for search_result in search_results:
                try:
                    results.append({
                        'title': ' '.join(search_result.find('a', {'class': 'title'}).text.split()),
                        'link': 'https://www.kijiji.ca/' + search_result.find('a', {'class': 'title'})['href'],
                        'id': search_result['data-listing-id'],
                        'price': search_result.find('div', {'class': 'price'}).text.strip(),
                    })
                except:
                    pass
            logger.info(
                f'{url}: {len(results)} results found in {round(time.time() - start_time, 2)} seconds')
            return results
        except Exception as e:
            logger.error(f'could not get search results. [{error_str(e)}]')
            return []

    def compare_search_results(self, url):
        search_results = self.search(url)
        if not self.urls[url]:
            self.urls[url] = search_results
            logger.info(f'setting new search results for: {url}')
        else:
            previous_ids = [u['id'] for u in self.urls[url]]
            for search_result in search_results:
                if search_result['id'] not in previous_ids:
                    if search_result['id'] not in self.notified_results:
                        logger.info(f'new search result found at: {url} [{search_result["title"]}]')
                        self.notify(search_result, url)
                        self.notified_results.append(search_result['id'])
                    else:
                        pass

    @staticmethod
    def notify(result, search_url):
        text = f'Title: {result["title"]}\n' \
               f'Price: {result["price"]}\n' \
               f'Search link: {search_url}\n' \
               f'Post link: {result["link"]}'
        try:
            message = MIMEMultipart()
            message['From'] = config.sender_email
            message['To'] = config.recipient_email
            message['Subject'] = 'New search result on Kijiji'
            message.attach(MIMEText(text, 'plain'))
            with smtplib.SMTP('smtp.gmail.com', 587) as session:
                session.starttls()
                session.login(config.sender_email, config.sender_password)
                session.sendmail(config.sender_email, config.recipient_email, message.as_string())
            print(f'email sent to {config.recipient_email}')
        except:
            print(f'could not send email to {config.recipient_email}')


def error_str(err):
    return ' '.join(str(err).split())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_id = sys.argv[1]
    else:
        input_id = ''

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
    while True:
        for url in kijiji.urls:
            try:
                kijiji.compare_search_results(url)
            except Exception as e:
                logger.error(error_str(e))