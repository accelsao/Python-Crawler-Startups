import requests
import re
from bs4 import BeautifulSoup
import os



class Pinterest:
    def __init__(self, cookie):
        self.base_url = 'https://www.pinterest.com'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'cookie' : cookie
        }

        self.mkdir('images')
        self.max_num = 10

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def get_urls(self, keyword):
        url = self.base_url + '/search/pins/?q=' + keyword
        # print(url)
        response = requests.get(url, headers=self.headers, verify=True)
        html = response.text
        # print(response)
        # print(html)
        srcSet = re.findall('(srcSet=".+? 4x")', html)
        num = 1
        for src in srcSet:
            # print(src)
            img_url = re.findall('(?<=3x, )https:.+?.(?:jpg|png)(?= 4x)', src) # 4x
            # print(img_url)
            if(len(img_url) != 1 or type(img_url) is not list):
                print(img_url)
                continue
            img_url = img_url[0]
            # print(img_url)
            with open('images/{}.jpg'.format(str(num).zfill(4)), "wb") as f:
                img_data = requests.get(img_url, headers=self.headers, verify=True).content
                f.write(img_data)
            print('Image{} download finished'.format(str(num).zfill(4)))
            num += 1



cookie = '_pinterest_cm=TWc9PSZEenVOcno5NWN5MUQ2NGx5TGN4U1hoR2xGY1NWZWtsWlI4VDcwQkIyQS9tZW0vMERQRmNVRUo5dFYwR0tSU3hRbUtXV0tpVGhlMmc0RzAvK0xQbTZDaVFoeXZIS01nd1phYkJwYW91ekN6Y0xER3VuZzM4Nmx0SEtTUHJHK2k3eCY5R1NyMkNZUUFEWCtCNCtUbW00L3ZoeXhMTEU9; _auth=1; csrftoken=Q6PP7J06F8YkIEkhr25UxNHcTSWfqWhf; _b="AT1z2QAaPe5I34xIdoeckW24rwIc9R9FcYRgSVnC3kS4QBcJLMJ925in8TAqrsKUL6Q="; cm_sub=none; _routing_id="ab0c6a9c-fded-48dc-af1d-3910da9b56fb"; sessionFunnelEventLogged=1; _pinterest_sess="TWc9PSZPTkFhcVFJelZpd1UwL0c4Z0tRcjU5THAyUGV5YlIyR2RCZ0dpQjBDWGpaVFNJczJXMlVaeGJybjl1N2xhQzZoL0Nvell0NkJxQVpYakdpRjZ6dFF4bWswQ25jUWNKWS9kL29tc2E1NXlUU0FnQTVMNXR5U1ljb24rdUdzTjFDMThmVG9sYXcybU1UZ1k3NG14OXRJTk5sVjVVNFVPTm5mTmtJTnhWdDJvbkhoQzdaemIyWURxUndzaVFWWm5hQVNJcDRUejRVMDFUVENBZVJVNmNxVTZtdWowRlVKL3h6VEFqbkpNU29ocFVwenI1QnppUDlHODI3eTg1MjZrcXgyWWRFa1BZNWUzL254TEpiVWRGOXBNdi9YTHVBK3V5Unc1dUFGd01PbGIyaVpkbHlpSnExNkxhRWgyd3pORTJWM00wV1JqTUcyalRsaVRDbDdIVUVuWVhPR2czc2VMSFFYb29ZT1EyK09zOVN4algzdXBsU05JMm9xbE5JcEQzTlFXeVVnLzVmNGNaU0J2eWpwZER1SWp3PT0mRm81T1N2OWNnZ2t4WEF1WTkzTXBvSFIzYW9BPQ==; bei=true'

pinterest = Pinterest(cookie)
pinterest.get_urls(keyword='鬼滅')