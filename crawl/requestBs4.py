import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

class RequestBs:
    def __init__(self, url=None, encoding='utf-8', headers=HEADERS):
        self.url = url
        self.headers = headers
        self.encoding = encoding
        self.session = requests.session()
        self.soup = None

    def get_response(self, response=None):
        return response if self.url == None else self.session.get(self.url, headers=self.headers)

    def get_soup(self, response=None):
        self.response = self.get_response(response)
        if self.response == None:
            assert Exception('error url or response')
        elif type(self.response) == str:
            self.soup = BeautifulSoup(self.response, 'html.parser')
        else:
            self.response.encoding = self.encoding
            self.soup = BeautifulSoup(self.response.text, 'html.parser')

        return self.soup

    def soup_get_element(self, element, rule='.*', response=None):
        content_list = []
        soup = self.get_soup(response)
        for i in soup.find_all(element):
            content_list.extend(re.findall(rule, str(i)))
        return remove_none(content_list)

    def complex_url_html(self, url, x)->str:
        if self.is_last_slash(url) and self.is_first_slash(x):
            return url[:-1] + x + '.html'
        elif not self.is_last_slash(url) and not self.is_first_slash(x):
            return url + '/' + x + '.html'

    def complex_url_path(self, url, x)->str:
        if self.is_last_slash(url) and self.is_first_slash(x):
            if self.is_last_slash(x):
                return url[:-1] + x
            else:
                return url[:-1] + x + '/'
        elif not self.is_last_slash(url) and not self.is_first_slash(x):
            if self.is_last_slash(x):
                return url + '/' + x
            else:
                return url + '/' + x + '/'
        elif not self.is_last_slash(url) and self.is_first_slash(x) or \
                self.is_last_slash(url) and not self.is_first_slash(x):
            if self.is_last_slash(x):
                return url + x
            else:
                return url + x + '/'

    def complex_url(self, url_path, element, rule, path=False, html=False)->str or list:
        new_url_list = []
        url = self.soup_get_element(element=element, rule=rule)
        if type(url) == list:
            if path:
                for i in url:
                    new_url_list.append(self.complex_url_path(url=url_path, x=i))
                return new_url_list
            elif html:
                for i in url:
                    new_url_list.append(self.complex_url_html(url=url_path, x=i))
                return new_url_list

    def is_last_slash(self, url):
        return True if url[-1] == '/' else False

    def is_first_slash(self, url):
        return True if url[0] == '/' else False

def remove_none(x:list) -> list:
    for i in x:
        if not i:
            x.remove(i)
            return remove_none(x)
    return x

def remove_tags(tags, text):
    return re.sub(tags, '', text)