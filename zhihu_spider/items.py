# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class ZhihuSpiderItem(scrapy.Item):
    user_name = scrapy.Field()  # 用户名
    followees = scrapy.Field()  # 用户粉丝
    followers = scrapy.Field()  # 用户关注的人
    introduce = scrapy.Field()  # 简介
    ellipsis = scrapy.Field()  # 用户详细介绍
    location = scrapy.Field()  # 住址
    major = scrapy.Field()  # 主修
    head_image = scrapy.Field()  # 头像url
    views = scrapy.Field()  # 浏览次数
    ask = scrapy.Field()  # 提问
    answer = scrapy.Field()  # 回答
    articles = scrapy.Field()  # 文章
    collected = scrapy.Field()  # 收藏
    public_editor = scrapy.Field()  # 公共编辑
    main_page = scrapy.Field()
    _id = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
