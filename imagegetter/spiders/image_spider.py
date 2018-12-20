# !/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy

class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()

class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['mzitu.com']
    start_urls = [
        "http://www.mzitu.com/xinggan/page/4/"
    ]
    page = 4
    count = 0
    MAX_CATCH_PAGE = 100
    item = ImageItem()

    def parse(self, response):
        # 获取所有网址
        next_page = response.xpath('//ul[@id="pins"]/li').re('https://www.mzitu.com/([0-9]+)')
        # 查重
        page = []
        for num in next_page:
            if num not in page:
                page.append(num)
        # 按主题爬取
        for case in page:
            open_url = "https://www.mzitu.com/%s" %case
            yield scrapy.Request(open_url, callback=self.image_url)

        if self.page<self.MAX_CATCH_PAGE:
            self.page = self.page + 1
        next_url = "http://www.mzitu.com/xinggan/page/%d" % self.page
        print next_url
        yield scrapy.Request(next_url, callback=self.parse)

    def image_url(self, response):
        # 获取所有地址
        max_page = response.xpath('//div[@class="pagenavi"]').re('span>([0-9]+)</span')
        target = int(response.url.split('/')[-1])
        # 获取页数
        max_num = 0
        for i in max_page:
            if int(i) > max_num:
                max_num = int(i)
        for i in xrange(1,max_num):
            open_url = "https://www.mzitu.com/%d/%d" % (target,i)
            self.item['url'] = open_url
            yield scrapy.Request(open_url, callback=self.post_page)

    def post_page(self, response):
        image_url = response.xpath('//div[@class="main-image"]//img/@src').extract()
        self.item['images'] = image_url
        return self.item



