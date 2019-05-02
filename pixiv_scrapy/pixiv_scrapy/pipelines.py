# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import json


class PixivMetaPipeline(object):
    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item)) + "\n")
        return item
    def open_spider(self, spider):
        settings = spider.settings
        file_path = settings['IMAGES_STORE']+'/meta.json'
        self.file = open(file_path,'w')
        self.file.write('[')
        return

    def close_spider(self,spider):
        self.file.write(']')
        self.file.close()
        return


class PixivImagesPipeline(ImagesPipeline):

    # def file_path(self, request, response=None, info=None):
    #     item = request.meta['item'] # Like this you can use all from item, not just url.
    #     return item['title'] + 'jpg'
    #     # image_guid = request.url.split('/')[-1]
    #     # return 'full/%s' % (image_guid)

    """抽取ITEM中的图片地址，并下载"""
    def get_media_requests(self, item, info):
        # print('Access get_media_requests !!')
        # print('item img_urls -> {}'.format(item['img_urls']))
        try:
            for image_url in item['img_urls']:
                # print('wtf???')
                # print(item['title'])
                # print(item['img_urls'])
                # print('image_url : {}'.format(image_url))
                yield scrapy.Request(
                    image_url,
                    headers={
                        'Referer': item['url'],  #添加Referer，否则会返回403错误
                        'User-Agent': 'Mozilla/5.0 (Macintosh; '
                        'Intel Mac OS X 10_10_5) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/45.0.2454.101 Safari/537.36'
                    }
                )

        except KeyError:
            raise DropItem("Item contains no images")

    def item_completed(self, results, item, info):
        # print('item completed')
        #image_paths这段都没看懂，Python好高深，大概意思是获取results列表中获取到图片的地址
        for ok, x in results:
            print(ok, x)
        image_paths = [x['path'] for ok, x in results if ok]
        # image_paths = item['title'] + '.jpg'
        # print(image_paths)
        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] = '123' + '.jpg'
        item['image_paths'] = image_paths
        # print('finish right?')
        # print(item)
        return item