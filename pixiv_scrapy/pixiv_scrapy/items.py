# -*- coding: utf-8 -*-

import scrapy


class PixivScrapyItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    rank = scrapy.Field()
    yes_rank = scrapy.Field()
    total_score = scrapy.Field()
    views = scrapy.Field()
    is_sexual = scrapy.Field()
    illust_id = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    image_paths = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
