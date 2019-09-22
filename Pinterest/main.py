# -*- coding=utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import os
from selenium import webdriver
import time
from utils import url_encode
from requests.structures import CaseInsensitiveDict
import json


class Pinterest:
    def __init__(self, cookie, img_start_idx, proxies=None, agent_string=None):
        self.home_page = 'https://www.pinterest.com'
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        self.cookie = cookie
        self.mkdir('images')
        self.max_num = 100
        self.scroll_down_num = 1
        self.http = requests.session()

        self.start_idx = img_start_idx
        self.proxies = proxies
        self.next_book_marks = {'pins': {}, 'boards': {}, 'people': {}}

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def request(self, method, url, params=None, data=None, files=None, headers=None, ajax=False, stream=None):
        _headers = CaseInsensitiveDict([
            ('Accept', 'text/html,image/webp,image/apng,*/*;q=0.8'),
            ('Accept-Encoding', 'gzip, deflate'),
            ('Accept-Language', 'en-US,en;q=0.8'),
            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
            ('Cache-Control', 'no-cache'),
            ('Connection', 'keep-alive'),
            ('Host', 'www.pinterest.com'),
            ('Origin', 'https://www.pinterest.com'),
            ('Referer', self.home_page),
            ('User-Agent', self.user_agent),
            ('Cookie', self.cookie)
        ])
        if method.upper() == 'POST':
            _headers.update([('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')])
        if ajax:
            _headers.update([('Accept', 'application/json')])
            csrftoken = self.http.cookies.get('csrftoken')
            if csrftoken:
                _headers.update([('X-CSRFToken', csrftoken)])
            _headers.update([('X-Requested-With', 'XMLHttpRequest')])
        if headers:
            _headers.update(headers)
        response = self.http.request(method, url, params=params, data=data, headers=_headers,
                                     files=files, timeout=60, proxies=self.proxies, stream=stream)
        return response

    def get(self, url, params=None, headers=None, ajax=False, stream=None):
        return self.request('GET', url=url, params=params, headers=headers, ajax=ajax, stream=stream)

    def search(self, scope, query):
        q = url_encode({
            'q': query,
            '_': '%s' % int(time.time() * 1000)
        })
        url = 'https://www.pinterest.com/search/{}/?q={}'.format(scope, query)
        print(url)
        response = self.get(url=url)

        # html = response.text
        html = response.text[response.text.find('application/json'):]
        # print(html)

        html = html[html.find('{'):html.find('}</script>') + 1]
        # print(html)
        search_result = json.loads(html)
        results = []
        # print(search_result)
        # print(search_result['resources']['data']['BaseSearchResource'])
        # print(search_result['resources']['data']['BaseSearchResource'].values())
        # print(len(search_result['resources']['data']['BaseSearchResource']))
        # print(next(iter(search_result['resources']['data']['BaseSearchResource'].values())))
        try:
            if len(search_result['resources']['data']['BaseSearchResource']):

                search_resource = next(iter(search_result['resources']['data']['BaseSearchResource'].values()))
                # print(search_resource)
                # print(search_resource['data'])
                # print(search_resource['data']['results'])
                results = search_resource['data']['results']
                # print(search_resource['nextBookmark'])
                self.next_book_marks[scope][query] = search_resource['nextBookmark']
        except KeyError:
            pass
        return results
        # html = re.findall('(?<="nextBookmark": )".+?",', html)
        # print(html)
        # try:
        #     if len(html):
        #         html = html[0][1:-2]
        #         print(html)
        #         self.next_book_marks[scope][query] = html
        # except:
        #     pass
    def __search_next_page(self, scope, query):
        if not self.next_book_marks[scope].get(query):
            return self.search(scope, query)

        q = url_encode({
            'source_url': '/search/{}/?q={}'.format(scope, query),
            'data': json.dumps({
                'options': {
                    'bookmarks': [self.next_book_marks[scope][query]],
                    'query': query,
                    'scope': scope
                },
                "context": {}
            }).replace(' ', ''),
            '_': '%s' % int(time.time() * 1000)
        })
        url = 'https://www.pinterest.com/resource/BaseSearchResource/get/?{}'.format(q)
        response = self.get(url=url, ajax=True).json()
        # print(response)
        results = []
        # for key, value in response['resource_response']['data'].items():
        #     print(key)
        # print(response['resource'])
        # print(response['resource_response']['data']['results'])
        try:
            if response['resource_response']['error'] is not None:
                error = response['resource_response']['error']
                raise Exception('[{}] {}'.format(error['http_status'], error['message']))
            results = response['resource_response']['data']['results']
            self.next_book_marks[scope][query] = response['resource']['options']['bookmarks']
        except KeyError:
            pass
        return results



    def search_pins(self, query, download_imgs=True):
        pins = []
        while len(pins) < self.max_num:
            results = self.__search_next_page('pins', query)
            for result in results:
                pins.append({
                    'url' : result['images']['orig']['url'],
                    'id' : result['id'],
                })
                # print(result['images']['orig']['url'])
                # print(result['id'])
        if download_imgs:
            images_url_list = list({dict['id']: dict['url'] for dict in pins}.values())
            num = self.start_idx
            for url in images_url_list:
                print(url)
                with open('images/{}.jpg'.format(str(num).zfill(4)), "wb") as f:
                    img_data = requests.get(url, headers={
                        'user-agent': self.user_agent,
                        'cookie': self.cookie
                    })
                    print(img_data)
                    img_data = img_data.content
                    f.write(img_data)
                print('Image{} download finished'.format(str(num).zfill(4)))
                num += 1
        return pins


cookie = '_pinterest_cm=TWc9PSZEenVOcno5NWN5MUQ2NGx5TGN4U1hoR2xGY1NWZWtsWlI4VDcwQkIyQS9tZW0vMERQRmNVRUo5dFYwR0tSU3hRbUtXV0tpVGhlMmc0RzAvK0xQbTZDaVFoeXZIS01nd1phYkJwYW91ekN6Y0xER3VuZzM4Nmx0SEtTUHJHK2k3eCY5R1NyMkNZUUFEWCtCNCtUbW00L3ZoeXhMTEU9; _b="AT1z2QAaPe5I34xIdoeckW24rwIc9R9FcYRgSVnC3kS4QBcJLMJ925in8TAqrsKUL6Q="; G_ENABLED_IDPS=google; logged_out=True; fba=True; _auth=1; cm_sub=none; sessionFunnelEventLogged=1; _pinterest_referrer="https://www.facebook.com/"; _ga=GA1.2.1393323950.1569118619; _gid=GA1.2.1754986104.1569118619; csrftoken=gRDX2LLPJfIQQCTc89xFJD1hrXWrGmgm; _routing_id="a006641c-5e3f-4a25-aeca-f2b95a8e6fda"; _pinterest_sess=TWc9PSZRSzBWRm9CalYwMkx5M1hIWmhlcWk3SEw4TTdqY0hJSER1Y1llTy80QWNqR3lXTmJ2cmNJUnRrbUtIekdJNHVhWkxlNGpZbEZTSTJDb0RTVVczbWFjUGtleGFza2ZMWVdIQmVQUktUM25qV3NQVjRFdWZ4aWIzYkt3a0RFNitWcXFFaml0YlYvQ001aFpyOWU1U0l2Zk9DcUt6dEZod08yZEphb1hEUnFMeWk2NjdSN1BGZmZSN0Z4RStuK05Sa2tBYUpHN0Z1UXQyM251cFNXNFU3aWVwa1U4OHFpbUtGNFFWOGpWU21SLzl4d1BqVXVXU29COGRJTEpBWUlnZTdlbm1uRXBZWmhSUWtLdmpiLytiZWdSYzc1ZGlZQml1a21pZVk1OFhtS1Mvak9XTHhQWlZZa0FTRm9ydTVxdWpoRDd4SCtpeUp6ekQ1T3M1S0ptN0RzOTJLR1FaK1Vabm5RMXpucUZBNXg3TENvMXYyWE4rd2F4MUd5em5ENGh5RGdheXFIVk5oQXhWaHh1d2hFNnFkRHB1bmNnVkZsalpnd25iT2lCZlhmaDg1SWd6UEFsUmlxdHNEZE8vTVhnY0lEdnBTSEJ3UXM1cmEwVUYvWi9GU09KTEVWaldGd0dwWnBaRlhnalg3VTJJaz0mcW05ZVhsM0xEdUhXRUd3a0FEaUZxand1M2FVPQ==; bei=false'
pinterest = Pinterest(cookie, img_start_idx=1)
pinterest.search_pins(query='cat')
