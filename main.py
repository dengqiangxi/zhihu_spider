#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/6/7
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 执行指定的spider
process.crawl('zhihu')

process.start()
