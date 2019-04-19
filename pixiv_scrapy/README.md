# Reference
1. https://stackoverflow.com/questions/38772662/scrapy-images-downloading

2. https://github.com/littleVege/pixiv_crawl

3. https://docs.scrapy.org/en/latest/intro/tutorial.html

# Need
pip install pypiwin32

pip install Pillow

pip install scrapy
# 需要用到的command

cd PycharmProjects/pixiv_scrapy

scrapy shell "https://accounts.pixiv.net/login?lang=zh_tw"

scrapy crawl pixiv

scrapy crawl pixiv -o pixiv.json