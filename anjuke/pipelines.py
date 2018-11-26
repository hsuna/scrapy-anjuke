# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

from scrapy.conf import settings
from anjuke.items import PageItem,HouseItem

import logging

class AnjukePipeline(object):
    def __init__(self):
        client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = client[settings['MONGODB_DB']]
        self.pageColl = db[settings['MONGODB_COLLECTION_PAGE']]
        self.houseColl = db[settings['MONGODB_COLLECTION_HOUSE']]

    def process_item(self, item, spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem('Missing{0}!'.format(data))
        if valid:
            if(isinstance(item, PageItem)):
                self.process_PageItem(item)
            elif(isinstance(item, HouseItem)):
                self.process_HouseItem(item)
        return item

    def process_PageItem(self, item):
        try:
            self.pageColl.insert(dict(item))
            logging.debug("记录页面%s"%item["page"])
        except Exception:
            logging.debug("页面《%s》已经爬过，跳过"%item["page"])

    def process_HouseItem(self, item):
        try:
            self.houseColl.insert(dict(item))
            logging.debug("插入数据[%s]"%item["house_id"])
        except Exception:
            logging.debug("数据[%s]已经存在"%item["house_id"])