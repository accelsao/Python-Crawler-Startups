# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json

class Dcard():
    def __init__(self):
        self.base_url = "https://www.dcard.tw/f"
        self.headers = {
            "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        session = requests.Session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        self.session = session

    def get_soup(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        return soup
    def get_title(self):
        url = self.base_url
        text = self.session.get(url).text
        soup = self.get_soup(text)
        dcard_title = soup.find_all('h3', re.compile('PostEntry_title_'))
        with open('Dcard Top 10 Hot post.txt', 'w', encoding='utf-8') as f:
            f.write("Dcard 熱門前十文章標題:\n")
            for idx, item in enumerate(dcard_title[:10], 1):
                f.write("Rank: {} - Title: {}\n".format(idx, item.text.strip()))
    def get_json(self, url):
        response = self.session.get(url)
        data = response.json()
        return data

# if __name__ == '__main__':
#     spider = Dcard()
#     spider.get_title()
#     json = spider.get_json('https://www.dcard.tw/_api/posts/231016024')
#     print(json)