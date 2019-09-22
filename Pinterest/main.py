# -*- coding=utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import os
from selenium import webdriver
import time


class Pinterest:
    def __init__(self, cookie):
        self.base_url = 'https://www.pinterest.com'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'cookie' : cookie
        }

        self.mkdir('images')
        self.max_num = 5
        self.scroll_down_num = 1
        self.driver = webdriver.Chrome('chromedriver')
        self.login_google_and_Pinterest()
        self.start_idx = 1

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def scroll_down(self):
        for i in range(self.scroll_down_num):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)



    def get_urls(self, start_idx, keyword):

        # last_idx = start_idx + self.max_num
        # while num < last_idx:

        url = self.base_url + '/search/pins/?q=' + keyword
        print(url)
        driver = self.driver
        # driver.get(url)
        # time.sleep(8)
        # login = driver.find_elements_by_xpath("//button[text()='以***的身分繼續使用']")
        # print(login)
        # if len(login) == 1:
        #     login[0].click()
        # # print(login)
        # # login[0].click()
        # # # driver.find_element_by_xpath("//button[text()='登入']").click()
        # # time.sleep(3)
        # # driver.find_element_by_link_text('以 Google 帳號繼續').click()
        # time.sleep(3)
        driver.get(url)
        time.sleep(3)

        cur_idx = self.start_idx

        for i in range(self.max_num):
            html = driver.page_source
            print(html)
            srcSet = re.findall('(srcset=".+? 4x")', html)
            print(srcSet)
            for src in srcSet:
                print(src)
                img_url = re.findall('(?<=3x, )https:.+?.(?:jpg|png)(?= 4x)', src)  # 4x
                if (len(img_url) != 1 or type(img_url) is not list):
                    print(img_url)
                    continue
                img_url = img_url[0]
                print(img_url)
                with open('images/{}.jpg'.format(str(cur_idx).zfill(4)), "wb") as f:
                    img_data = requests.get(img_url, headers=self.headers, verify=True).content
                    f.write(img_data)
                print('Image{} download finished'.format(str(cur_idx).zfill(4)))
                cur_idx += 1
            self.scroll_down()




        # soup = BeautifulSoup(html, 'lxml')
        # print(soup)


        # srcSet = re.findall('(srcSet=".+? 4x")', html)
        # # srcSet = soup.find_all(text=re.compile('(srcSet=".+? 4x")'))
        # print(srcSet)
        # num = self.cur_idx
        # for src in srcSet:
        #     print(src)
        #     img_url = re.findall('(?<=3x, )https:.+?.(?:jpg|png)(?= 4x)', src)  # 4x
        #     if (len(img_url) != 1 or type(img_url) is not list):
        #         print(img_url)
        #         continue
        #     img_url = img_url[0]
        #     print(img_url)
        #     with open('images/{}.jpg'.format(str(num).zfill(4)), "wb") as f:
        #         img_data = requests.get(img_url, headers=self.headers, verify=True).content
        #         f.write(img_data)
        #     print('Image{} download finished'.format(str(num).zfill(4)))
        #     num += 1
        # if num < 100:
        #     self.scroll_down()
        # self.cur_idx = num
        #
        # # driver.impli
        # # content =
        # # print(html)


        # response = requests.post(url, data=data, headers=self.headers).text
        # headers = self.headers
        # headers['referer'] = 'https://www.pinterest.com/'
        # response = requests.post(url, data=data, headers=headers).text
        # print(response)
        # print(html)
        # img_set = re.findall('(?="orig": {"url": )".+?"(?<=, "width")', html)
        # for num, img_src in enumerate(img_set, 1):
        #     img_url = re.findall('h.+g', img_src)
        #     if len(img_url):
        #         img_url = img_url[0]
        #         with open('images/{}.jpg'.format(str(num).zfill(4)), "wb") as f:
        #             img_data = requests.get(img_url, headers=self.headers, verify=True).content
        #             f.write(img_data)
        #         print('Image{} download finished'.format(str(num).zfill(4)))

    def login_google_and_Pinterest(self):
        driver = self.driver
        driver.get('https://accounts.google.com/signin')
        account = driver.find_element_by_xpath("//input[@id='identifierId']")
        account.send_keys('***')
        driver.find_element_by_id("identifierNext").click()
        time.sleep(5)
        password = driver.find_element_by_xpath("//input[@name='password']")
        password.send_keys("***")
        driver.find_element_by_id("passwordNext").click()
        time.sleep(5)
        url = self.base_url
        driver.get(url)
        time.sleep(5)
        login = driver.find_elements_by_xpath("//button[text()='***']")
        if len(login) == 1:
            login[0].click()



cookie = '_pinterest_cm=TWc9PSZEenVOcno5NWN5MUQ2NGx5TGN4U1hoR2xGY1NWZWtsWlI4VDcwQkIyQS9tZW0vMERQRmNVRUo5dFYwR0tSU3hRbUtXV0tpVGhlMmc0RzAvK0xQbTZDaVFoeXZIS01nd1phYkJwYW91ekN6Y0xER3VuZzM4Nmx0SEtTUHJHK2k3eCY5R1NyMkNZUUFEWCtCNCtUbW00L3ZoeXhMTEU9; _auth=1; csrftoken=Q6PP7J06F8YkIEkhr25UxNHcTSWfqWhf; _b="AT1z2QAaPe5I34xIdoeckW24rwIc9R9FcYRgSVnC3kS4QBcJLMJ925in8TAqrsKUL6Q="; cm_sub=none; _routing_id="ab0c6a9c-fded-48dc-af1d-3910da9b56fb"; sessionFunnelEventLogged=1; _pinterest_sess="TWc9PSZPTkFhcVFJelZpd1UwL0c4Z0tRcjU5THAyUGV5YlIyR2RCZ0dpQjBDWGpaVFNJczJXMlVaeGJybjl1N2xhQzZoL0Nvell0NkJxQVpYakdpRjZ6dFF4bWswQ25jUWNKWS9kL29tc2E1NXlUU0FnQTVMNXR5U1ljb24rdUdzTjFDMThmVG9sYXcybU1UZ1k3NG14OXRJTk5sVjVVNFVPTm5mTmtJTnhWdDJvbkhoQzdaemIyWURxUndzaVFWWm5hQVNJcDRUejRVMDFUVENBZVJVNmNxVTZtdWowRlVKL3h6VEFqbkpNU29ocFVwenI1QnppUDlHODI3eTg1MjZrcXgyWWRFa1BZNWUzL254TEpiVWRGOXBNdi9YTHVBK3V5Unc1dUFGd01PbGIyaVpkbHlpSnExNkxhRWgyd3pORTJWM00wV1JqTUcyalRsaVRDbDdIVUVuWVhPR2czc2VMSFFYb29ZT1EyK09zOVN4algzdXBsU05JMm9xbE5JcEQzTlFXeVVnLzVmNGNaU0J2eWpwZER1SWp3PT0mRm81T1N2OWNnZ2t4WEF1WTkzTXBvSFIzYW9BPQ==; bei=false'

pinterest = Pinterest(cookie)
pinterest.get_urls(start_idx=1, keyword='cat')

# google account and password , use *** identity to continue




