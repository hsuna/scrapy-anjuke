# -*- coding: utf-8 -*-

import re

from pymongo import MongoClient

import scrapy
from scrapy.conf import settings
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from anjuke.items import PageItem, HouseItem


class AnjukeSpider(CrawlSpider):
    name = 'anjuke'
    start_urls = ['https://m.anjuke.com/gz/sale/']
    custom_settings = {
        #"DOWNLOAD_DELAY": 5,
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Eanguage': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        }
    }
    dont_redirect = True
    handle_httpstatus_list = [302]

    def __init__(self):
        client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = client[settings['MONGODB_DB']]
        self.pageColl = db[settings['MONGODB_COLLECTION_PAGE']]
        self.houseColl = db[settings['MONGODB_COLLECTION_HOUSE']]

    def start_requests(self):
        for i in range(1, 60):
            url = 'https://m.anjuke.com/gz/sale/?from=anjuke_home&page='+str(i)
            result = self.pageColl.find_one({'page_url': url})
            if result:
                urls = result['house_urls']
                for url in urls:
                    if self.check_url(url):
                        yield scrapy.Request(url, callback=self.parse_item)
            else:
                yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        selector = Selector(response)
        urls = selector.xpath('//a[contains(@class, "house-item")]/@href').extract()
        
        item = PageItem()
        item['page'] = re.match(r'.*&page=(\d*).*', response.url, re.M | re.I).group(1)
        item['page_url'] = response.url
        item['house_urls'] = urls
        yield item

        for url in urls:
            if self.check_url(url):
                yield scrapy.Request(url, callback=self.parse_item)

    def check_url(self, url):
        house_id = re.match(r'.*/gz/sale/(\w*).*', url, re.M | re.I)
        if str(house_id) == 'None':
            return False
        else:
            result = self.houseColl.find_one({'house_id': house_id.group(1)})
            if result:
                return False
            else:
                return True

    def parse_item(self, response):
        selector = Selector(response)
        housebasic = selector.xpath('//div[@class="house-info-content"]')
        if len(housebasic.extract()) > 0:
            # 存放房子信息
            item = HouseItem()
            item['house_id'] = re.match(r'.*/gz/sale/(\w*).*', response.url, re.M | re.I).group(1)
            item['title'] = housebasic.xpath('normalize-space(./div[@class="house-address"]/text())').extract()[0]
            item['tolprice'] = housebasic.xpath('normalize-space(./div[@class="house-data"]/span[1]/text())').extract()[0]
            item['mode'] = housebasic.xpath('normalize-space(./div[@class="house-data"]/span[2]/text())').extract()[0]
            item['area'] = housebasic.xpath('normalize-space(./div[@class="house-data"]/span[3]/text())').extract()[0]

            names = [
                'price',
                'orientation',
                'floor',
                'decorate',
                'built',
                'house_type',
                'agelimit',
                'elevator',
                'only',
                'budget',
                'district',
                'traffic',
            ]
            houseinfo = selector.xpath('//ul[@class="info-list"]/li')
            for i, info in enumerate(houseinfo):
                name = names[i]
                text = info.xpath('normalize-space(./text())').extract()
                a_text = info.xpath('normalize-space(./a[1]/text())').extract()
                if name == 'budget':
                    item[name] = a_text[0]
                elif name == 'district':
                    item[name] = a_text[0] + text[0]
                else:
                    item[name] = text[0]
            # print(item)
            return item
