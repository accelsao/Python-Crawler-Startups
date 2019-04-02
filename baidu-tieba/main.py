#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests


class TiebaSpider():
    def __init__(self, kw, max_pn):
        self.max_pn = max_pn
        self.kw = kw;
        self.base_url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}"
        self.headers = {
            "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
    def run(self):
        url_list = self.get_url_list()
        for idx, url in enumerate(url_list, 1):
            # print(url)
            content = self.get_content(url)

            items = self.get_items(content, idx)
            self.save_items(items)

    def get_url_list(self):
        url_list = []
        for pn in range(0, self.max_pn, 50):
            url = self.base_url.format(self.kw, pn)
            url_list.append(url)
        return url_list

    def get_content(self, url):
        reponse = requests.get(
            url = url,
            headers = self.headers
        )
        return reponse.content

    def get_items(self, content, idx):
        # print(content.title())
        with open("08-{}.html".format(idx), 'wb') as f:
            f.write(content)


    def save_items(self, items):
        pass


if __name__ == '__main__':
    spider = TiebaSpider("英雄联盟", 200)
    spider.run()