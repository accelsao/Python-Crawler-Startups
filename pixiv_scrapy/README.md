# TODO
- [ ] Customize filename Title w/o full/hash [here](https://stackoverflow.com/questions/18081997/scrapy-customize-image-pipeline-with-renaming-defualt-image-name)
- [ ] Find by author_id
- [ ] Find Keyword
- [ ] Learn MiddleWare

# Reference
1. [Scrapy Images Downloading - StackOverflow](https://stackoverflow.com/questions/38772662/scrapy-images-downloading)

2. [littleVege/pixiv_crawl](https://github.com/littleVege/pixiv_crawl)

3. [Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)

4. [Scrapy 1.6 documentation](https://docs.scrapy.org/en/latest/index.html)

# Installation
pip install pypiwin32

pip install Pillow

pip install scrapy
# Scrapy Command tips

cd PycharmProjects/pixiv_scrapy

scrapy crawl pixiv

scrapy shell "https://accounts.pixiv.net/login?lang=zh_tw"

scrapy crawl pixiv -o pixiv.json

# User Configuration
* IMAGES_STORE 圖片位置
* PIXIV_USER_NAME 帳號
* PIXIV_USER_PASS 密碼
* START_DATE 開始時間
* SELECT_MODE_IDX 模式選擇
