import requests
import re
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import os

class IG_Crawler:
    def __init__(self):
        self.base_url = 'https://www.instagram.com/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.mkdir('images')
        self.max_num = 10

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def get_urls(self, keyword):
        url = self.base_url + keyword + '/'
        response = requests.get(url, headers=self.headers).text
        short_codes_lists = re.findall('"shortcode":(.+?),', response)
        num = 1
        for id, code in enumerate(short_codes_lists):
            if id == self.max_num:
                break
            url = 'https://instagram.com/p/{}/'.format(code[1:-1])
            print(url)
            # https://instagram.ftpe8-2.fna.fbcdn.net/vp/f5da9f405ef7728396a74f6cadece0aa/5E076687/t51.2885-15/e35/s1080x1080/69040385_2371942819562545_1575170158448228648_n.jpg?_nc_ht=instagram.ftpe8-2.fna.fbcdn.net&_nc_cat=101
            response = requests.get(url).text
            # print(response)
            img_url = re.findall('"display_url":"(.+?)",', response)[0]
            img_url = img_url.split('\\')[0]
            # print(img_url)
            with open('images/{}.jpg'.format(str(num).zfill(4)), "wb") as f:
                img_data = requests.get(img_url).content
                f.write(img_data)
            num += 1
        # print(response)


# https://instagram.ftpe8-2.fna.fbcdn.net/vp/f5da9f405ef7728396a74f6cadece0aa/5E076687/t51.2885-15/e35/s1080x1080/69040385_2371942819562545_1575170158448228648_n.jpg?_nc_ht=instagram.ftpe8-2.fna.fbcdn.net\u0026_nc_cat=101
ig = IG_Crawler()
ig.get_urls(keyword='yuniko0720')
