#!/usr/bin/env python
# -*- coding=utf8 -*-
# Created by dengqiangxi at 2018/11/5
import pymysql

# 数据库相关配置
mysql_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'toor',
    'db': 'zhihu',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}