import requests

from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

class Crawl:
    def __init__(self, url):
        self.url = url
        self.session = requests.session()

    def get_soup(self):
        self.response = self.session.get(self.url, headers=HEADERS)
        self.response.encoding = 'UTF-8'
        soup = BeautifulSoup(self.response.text, 'html.parser')
        return soup

class Alchemy():
    pass