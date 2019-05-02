# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from scrapy.exceptions import *
from pixiv_scrapy.items import PixivScrapyItem
import re
import os

class PixivSpider(scrapy.Spider):
    name = 'pixiv'
    allowed_domains = ['www.pixiv.net', 'accounts.pixiv.net']
    start_urls = ['http://www.pixiv.net/']

    # print(datetime.date(2015,9,10))
    # print(datetime.datetime(2019, 4, 1))
    # os.system('PAUSE')
    # 開始登陸 需要post_key
    def start_requests(self):



        return [scrapy.Request(url='https://accounts.pixiv.net/login',callback=self.get_post_key)]

    def get_post_key(self, response):
        post_key = response.css('[id=old-login] input[name=post_key]::attr(value)').extract_first()
        setting = self.settings
        if not setting['PIXIV_USER_NAME'] or not setting['PIXIV_USER_PASS']:
            raise CloseSpider('Username or Password Error!!!')
        return scrapy.FormRequest(url='https://accounts.pixiv.net/login',
                           formdata={
                               'pixiv_id': setting['PIXIV_USER_NAME'],
                               'password': setting['PIXIV_USER_PASS'],
                               'post_key': post_key,
                               'skip': '1', # what is this?
                               'mode': 'login' # necessary?
                           },
                           callback=self.logged_in)

    def logged_in(self, response):
        if response.url == 'https://accounts.pixiv.net/login':
            raise CloseSpider('username or password error!!!')
        print('Sucessfully Login')
        yield scrapy.Request(self.generate_list_url(self.settings['START_DATE']), callback=self.parse)

    def parse(self, response):
        result = json.loads(response.body, encoding='utf-8')
        # Use google chrome extentions for json viewer
        # "contents"
        # "mode": "daily",
        # "content": "all",
        # "page": 10,
        # "prev": 9,
        # "next": false,
        # "date": "20150910",
        # "prev_date": "20150909",
        # "next_date": "20150911",
        # "rank_total": 500
        # print('Result: {}'.format(result))
        # os.system("PAUSE")
        for section in result['contents']:
            item = PixivScrapyItem()
            print('Section: {}'.format(section))
            item['title'] = section['title']
            item['date'] = section['date']
            item['user_id'] = section['user_id']
            item['user_name'] = section['user_name']
            item['illust_id'] = section['illust_id']
            item['tags'] = section['tags']
            item['rank'] = section['rank']
            item['yes_rank'] = section['yes_rank']
            item['rating_count'] = section['rating_count']
            item['views'] = section['view_count']
            item['is_sexual'] = section['illust_content_type']['sexual']

            # section: {'title': '艦娘背比べ', 'date': '2015年09月09日 02:48',
            #           'tags': ['艦これ', '絵師の世界', '艦隊これくしょん', ' 身長', '愛', 'ラバウルの女神', '艦娘背比べ', '陸奥', '背比べ',
            #                    '艦これ10000users入り'],
            #           'url': 'https://i.pximg.net/c/240x480/img-master/img/2015/09/09/02/48/06/52438234_p0_master1200.jpg',
            #           'illust_type': '0', 'illust_book_style': '0', 'illust_page_count': '5', 'user_name': 'こずみっく',
            #           'profile_img': 'https://i.pximg.net/user-profile/img/2019/03/27/16/30/16/15574273_1360caf1f150970e1bd710e09ab1159d_50.jpg',
            #           'illust_content_type': {'sexual': 0, 'lo': False, 'grotesque': False, 'violent': False,
            #                                   'homosexual': False, 'drug': False, 'thoughts': False,
            #                                   'antisocial': False, 'religion': False, 'original': False, 'furry': False,
            #                                   'bl': False, 'yuri': False}, 'illust_series': False,
            #           'illust_id': 52438234, 'width': 1847, 'height': 850, 'user_id': 446127, 'rank': 1, 'yes_rank': 10,
            #           'rating_count': 977, 'view_count': 91012, 'illust_upload_timestamp': 1441734486, 'attr': '',
            #           'is_bookmarked': False, 'bookmarkable': True}
            # print(section['url'])
            # print(response.url)
            yield scrapy.Request(
                self.generate_detail_url(section['illust_id']),
                callback=self.parse_detail,
                meta={'item': item},
                headers={
                    'referer': response.url,
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
                }
            )

            # os.system('PAUSE')
        if result['next']:
            url = self.generate_list_url(self.settings['START_DATE'], result['next'], self.settings['SELECT_MODE'])
            yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        # print('response.meta: {}'.format(response.meta))
        # print(response)
        item['url'] = response.url
        # print('reponse.url : {}'.format(response.url))
        # os.system('PAUSE')
        html = response.text
        img_src = re.search('"regular":"(.+?)",',html).group(1)
        img_src = img_src.replace('\\', '')
        # print('img_src: {}'.format(img_src))
        # print('img_url: {}'.format(img_url))
        # print('item: {}'.format(item))
        # print('Maybe This ??!!')
        if (len(img_src) > 0):
            item['img_urls'] = [img_src] # wrap in list for piplines loop
        yield item

    def generate_detail_url(self, illust_id):
        return 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'.format(illust_id)


    def str_date(self, date=datetime.date.today()):
        return '{year}{month}{day}'.format(year=date.year, month=str(date.month).zfill(2), day=str(date.day).zfill(2))

    def generate_list_url(self, date=datetime.datetime.today().date(), page=1, mode='daily'):
        if (date != datetime.datetime.today().date()):
            str_date = self.str_date(date)
            print('str_date: {}'.format(str_date))
            url = 'http://www.pixiv.net/ranking.php?mode={mode}&date={str_date}&p={page}&format=json'.format(str_date=str_date, page=page, mode=mode)
        else:
            url = 'http://www.pixiv.net/ranking.php?mode={mode}&p={page}&format=json'.format(page=page, mode=mode)
        os.system('PAUSE')
        return url
