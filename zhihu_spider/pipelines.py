# -*- coding: utf-8 -*-

# Define your item pipelines here
#
import pymongo
import pymysql

from zhihu_spider.misc.all_secret_set import mysql_config
import logging
from zhihu_spider.misc.mysql_pool import ConnectionPool
from zhihu_spider.items import *
from scrapy.exceptions import DropItem
from zhihu_spider.misc.tools import spelling_insert_sql, hump2underline

item_class_list = [
    UserInfo,
    Business,
    Location,
    Topic,
    Following,
    Follower,
    Employment,
    Education,
]


class ZhihuSpiderPipeLine(object):

    def __init__(self):
        pool = ConnectionPool(size=20, name='pool', **mysql_config)
        self.connections = pool.get_connection()

    def process_item(self, item, spider):
        for item_class in item_class_list:
            if isinstance(item, item_class):
                self.save_item(item, hump2underline(item_class.__name__))

    def save_item(self, item, table_name):
        sql = spelling_insert_sql(item.keys(), table_name)
        try:
            with self.connections.cursor() as cursor:
                cursor.execute(sql, dict(item))
        except pymysql.err.MySQLError as e:
            logging.error(e)
            logging.warning("error item %s", item.__class__.__name__)
            self.connections.ping(reconnect=True)
            self.connections.rollback()
        except Exception as e:
            logging.error(e)
            raise DropItem('item exception', sql)

    def close_spider(self, spider):
        self.connections.close()
