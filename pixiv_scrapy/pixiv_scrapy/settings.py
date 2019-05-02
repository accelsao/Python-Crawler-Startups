# -*- coding: utf-8 -*-

# Scrapy settings for pixiv_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import datetime

BOT_NAME = 'pixiv_scrapy'

SPIDER_MODULES = ['pixiv_scrapy.spiders']
NEWSPIDER_MODULE = 'pixiv_scrapy.spiders'


ITEM_PIPELINES = {
    'pixiv_scrapy.pipelines.PixivImagesPipeline': 1,
    'pixiv_scrapy.pipelines.PixivMetaPipeline': 10
}
IMAGES_STORE = 'pixiv_scrapy/images/'

#########USER INFO
PIXIV_USER_NAME = ''
PIXIV_USER_PASS = ''

# START_DATE = datetime.datetime.today().date()
START_DATE = datetime.date(2019, 4, 1)


__PIXIV_MODES__ = [
    'daily',        #0 每日热榜
    'weekly',       #1 每周热榜
    'monthly',      #2 每月热榜
    'male',         #3 男性关注
    'female',       #4 女性关注
    'daily_r18',    #5 福利
    'weekly_r18',   #6 福利
    'male_r18',     #7 福利
    'female_r18'    #8 福利
]
__SELECT_MODE_IDX__ = 6 #在此设置对应索引号
SELECT_MODE = __PIXIV_MODES__[__SELECT_MODE_IDX__]  #无需设置，自动生成，供程序使用
########GENERATE IMAGE STORE
IMAGES_STORE = IMAGES_STORE + '{mode}/{year}{month}{day}'.format(
                        year=START_DATE.year,
                        month=str(START_DATE.month).zfill(2),
                        day=str(START_DATE.day).zfill(2),
                        mode = SELECT_MODE
                )


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pixiv_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'pixiv_scrapy.middlewares.PixivScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'pixiv_scrapy.middlewares.PixivScrapyDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'pixiv_scrapy.pipelines.PixivScrapyPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
