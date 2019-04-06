# -*- coding=utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import os
import heapq


class Pixiv():
    def __init__(self):
        self.session = requests.Session()
        self.base_url = 'https://www.pixiv.net'
        self.login_url = 'https://accounts.pixiv.net/login' #
        self.post_url = 'https://accounts.pixiv.net/api/login?lang=en' # login之後查看 XHR 找到 'login?lang=en'
        self.target_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self.post_key = self.get_post_key()
        self.pixiv_id = 'sayuri002'
        self.password = ''
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

    def get_keyword_topN(self, search_keyword=None, page_num=10, bookmarkThreshold=10000):
        keyword = str(search_keyword.encode('utf-8'))[2:-1].replace('\\x','%')
        # print(keyword)
        url = 'https://www.pixiv.net/search.php?word={}&order=date_d&p='
        image_list = []
        for page in range(page_num):
            target_url = url.format(keyword) + str(page + 1)
            # print(target_url)
            html = self.session.get(target_url, headers=self.headers).text
            # print(html)
            soup = BeautifulSoup(html, 'lxml')
            # print(soup)
            data_list = soup.find_all('input', {'id': 'js-mount-point-search-result-list'})[0] # 大膽假設每頁只有一個result list
            data = data_list['data-items']
            # print(data)
            id_list = re.findall('"illustId":"(.+?)"', data)

            for id in id_list:
                id_url = self.target_url.format(id)
                # print(id_url)
                html = self.session.get(id_url, headers=self.headers).text
                # print(html)
                img_bookmarkCount = re.search('"bookmarkCount":(\d+),', html).group(1)
                if int(img_bookmarkCount) < bookmarkThreshold:
                    continue
                # print(img_bookmarkCount)
                img_src = re.search('"regular":"(.+?)",', html).group(1)
                img_src = img_src.replace('\\', '')
                img_title = re.search('title>(.*?)】「(.*?)」', html).group(2)
                # print(img_src)
                # print(img_title)
                # image_list.append({
                #     'url': img_src,
                #     'title': img_title,
                #     'bookmarkCount': int(img_bookmarkCount),
                #     'href': id_url
                # })
                self.download_image(img_src, img_title, id_url)
            print('Page {} Finished'.format(page + 1))
        # image_list = sorted(image_list, key=lambda k: k['bookmarkCount'], reverse=True)
        # for a in image_list:
        #     self.download_image(a['url'], a['title'], a['href'])
            # print(a['bookmarkCount'])
            #     self.download_image(img_src, img_title, id_url)







pixiv = Pixiv()
# pixiv.get_ranking(img_num=10)
pixiv.get_keyword_topN('少女前線', page_num=8, bookmarkThreshold=1000)  # 超慢

