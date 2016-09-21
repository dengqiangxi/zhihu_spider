# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from zhihu_spider.items import ZhihuSpiderItem
from scrapy.exceptions import DropItem

class ZhihuSpiderPipeLine(object):
    def __init__(self):
        import pymongo
        connection = pymongo.MongoClient('127.0.0.1', 27017)
        self.db = connection["zhihu"]
        self.zh_user = self.db['zh_user']

    def process_item(self, item, spider):
        if isinstance(item, ZhihuSpiderItem):
            self.saveOrUpdate(self.zh_user, item)
            # print item
            # return item

    def saveOrUpdate(self, collection, item):
        try:
            collection.insert(dict(item))
            return item
        except:
            raise DropItem('重复喽')