#!/usr/bin/env python
# -*- coding=utf8 -*-
# Created by dengqiangxi at 2018/11/7

from zhihu_spider.misc.all_secret_set import mysql_config
import pymysql

__all__ = ['db_location_names', 'db_business_names', 'db_topic_names', 'db_user_ids', 'db_education_names',
           'db_employ_names']
connect = pymysql.connect(**mysql_config)


def get_data(table_name, distinct_key):
    with connect.cursor() as cursor:
        cursor.execute("select %s as `key` from %s" % (distinct_key, table_name))
        return {x['key'] for x in cursor.fetchall()}


db_location_names = get_data('location', 'name')
db_business_names = get_data('business', 'name')
db_topic_names = get_data('topic', 'name')
db_employ_names = get_data('employment', 'name')
db_user_ids = get_data('user_info', 'id')
db_education_names = get_data('education', 'name')
