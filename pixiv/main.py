# -*- coding=utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import os

class Pixiv():
    def __init__(self):
        self.session = requests.Session()
        self.base_url = 'https://www.pixiv.net'
        self.login_url = 'https://accounts.pixiv.net/login' #
        self.post_url = 'https://accounts.pixiv.net/api/login?lang=en' # login之後查看 XHR 找到 'login?lang=en'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self.post_key = self.get_post_key()
        self.pixiv_id = '***'
        self.password = '***'
        self.return_to = 'https://www.pixiv.net/'

        self.ranking_url = 'https://www.pixiv.net/ranking.php'
        self.load_path = 'image'
        self.mkdir(self.load_path)
        self.login()

    def get_post_key(self):
        page = self.session.get(self.login_url, headers=self.headers).text # text -> unicode, content -> bytes ref: http://www.python-requests.org/en/latest/api/#classes
        soup = BeautifulSoup(page, 'lxml')
        return soup.find('input')['value']


    def login(self):
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'return_to': self.return_to,
            'post_key': self.post_key
        }
        reqs = self.session.post(self.post_url, data=data, headers=self.headers)
        print('Login Message: ' + str(reqs.json()))

    def get_image(self, html):
        soup = BeautifulSoup(html, 'lxml')
        thumbnail = soup.find_all('div', {'class': '_layout-thumbnail'})
        print()
    def download_image(self, url, title, href):
        src_headers = self.headers
        src_headers['Referer'] = href
        print('Url: {}, Title: {}'.format(url,title))
        image = None
        try:
            html = requests.get(url, headers=src_headers)
            image = html.content
        except:
            print('Fail to load image')

        with open('image/' + title + '.jpg', 'ab') as f:
            f.write(image)
        print('{}.jpg sucessfully saved'.format(title))


    def get_ranking(self, mode='weekly', img_num=50):
        html = self.session.get(self.ranking_url + '?mode={}'.format(mode), headers = self.headers).text
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.find_all('div', {'class': 'ranking-image-item'})
        url_list = [div.a['href'] for div in divs][:img_num]
        for url in url_list:
            html = self.session.get(self.base_url + url).text
            img_src = re.search('"regular":"(.+?)",',html).group(1)
            img_src = img_src.replace('\\', '')
            # print(html)
            img_title = re.search('title>【(.*?)】「(.*?)」',html).group(2)
            # print(img_title)
            self.download_image(img_src, img_title, self.base_url + url)

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)


pixiv = Pixiv()
pixiv.get_ranking(img_num=10)
