#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json

# 定义请求url
url = "https://movie.douban.com/j/search_subjects"
# 定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}
# 循环构建请求参数并且发送请求
for page_start in range(0, 100, 20):
    params = {
        "type": "movie",
        "tag": "热门",
        "sort": "recommend",
        "page_limit": "20",
        "page_start": page_start
    }
    response = requests.get(
        url=url,
        headers=headers,
        params=params,
    )
    results = response.json()

    with open("movie_data.txt", 'w', encoding='utf-8') as f:
        for movie in results["subjects"]:
            # print(movie["title"], movie["rate"])
            f.write("title: {},  rank: {}\n".format(movie["title"], movie["rate"]))



# pycharm 2019.1 才不會有Error
# https://stackoverflow.com/a/54211170/8322368
