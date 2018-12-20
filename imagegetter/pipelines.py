# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class SaveImagesPipeline(ImagesPipeline):
    headers = {
        'USER-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Cookie': 'b963ef2d97e050aaf90fd5fab8e78633',
    }

    def get_media_requests(self, item, info):
        self.headers['Referer'] = item['url']
        for image_url in item['images']:
            yield scrapy.Request(image_url, headers=self.headers)
