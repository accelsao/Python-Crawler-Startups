# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class PixivImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        try:
            for url in item['iimage_urls']:
                yield scrapy.Request(
                    url,
                    headers={
                        'Referer': item['url'],
                        'User-Agent': 'Mozilla/5.0 (Macintosh; '
                                      'Intel Mac OS X 10_10_5) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/45.0.2454.101 Safari/537.36'
                    }
                )
        except KeyError:
            raise DropItem("Image Not Found, maybe get the wrong url")

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
