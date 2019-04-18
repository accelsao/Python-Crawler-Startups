# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from scrapy.exceptions import *
from pixiv_scrapy.items import PixivScrapyItem


class PixivSpider(scrapy.Spider):
    name = 'pixiv'
    allowed_domains = ['www.pixiv.net', 'accounts.pixiv.net']
    start_urls = ['http://www.pixiv.net/']

    def start_requests(self):
        # print('I am here--------------------------------start_requests')
        return [scrapy.Request(url='https://accounts.pixiv.net/login',callback=self.get_post_key)]

    def get_post_key(self, response):
        print('I am here--------------------------------getpostkey')
        post_key = response.css('[id=old-login] input[name=post_key]::attr(value)').extract_first()
        # post_key = response.css('#old-login input[name=post_key]::attr(value)').extract_first()

        setting = self.settings
        if not setting['PIXIV_USER_NAME'] or not setting['PIXIV_USER_PASS']:
            raise CloseSpider('username or password error!!!')
        # print('I am here--------------------------------I pass the account')
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
        for section in result['contents']:
            print('section: {}'.format(section))
            item = PixivScrapyItem()
            item['title'] = section['title']
            item['date'] = section['date']
            item['user_id'] = section['user_id']
            item['user_name'] = section['user_name']
            item['illust_id'] = section['illust_id']
            item['tags'] = section['tags']

            print('Go to Request per image')
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
        # if result['next']:
        #     url = self.generate_list_url(self.settings['START_DATE'], result['next'], self.settings['SELECT_MODE'])
        #     yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        print('response.meta: {}'.format(response.meta))
        item['url'] = response.url
        img_url = response.css('._illust_modal img').css('::attr("data-src")').extract()
        if (len(img_url) > 0):
            item['img_urls'] = img_url
        yield item

    def generate_detail_url(self, illust_id):
        return 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'.format(illust_id)


    def str_date(self, date=datetime.date.today()):
        return '{year}{month}{day}'.format(year=date.year, month=str(date.month).zfill(2), day=str(date.day).zfill(2))
    def generate_list_url(self, date=datetime.date.today(), page=1, mode='daily'):
        url_tmpl = 'http://www.pixiv.net/ranking.php?mode={mode}&date={str_date}&p={page}&format=json'
        if (isinstance(date, datetime.date)):
            str_date = self.str_date(date)
        else:
            str_date = date
        print('date: {}'.format(str_date))
        url = url_tmpl.format(str_date=str_date, page=page, mode=mode)
        print('url: {}'.format(url))
        return url
