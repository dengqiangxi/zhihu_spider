# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuSpiderItem(scrapy.Item):
    name = scrapy.Field()  # 用户名
    gender = scrapy.Field()  # 用户性别
    followees = scrapy.Field()  # 用户粉丝
    followers = scrapy.Field()  # 用户关注的人
    # headline = scrapy.Field()  # 简介
    detail_introduce = scrapy.Field()  # 用户详细介绍
    location = scrapy.Field()  # 住址
    major = scrapy.Field()  # 主修
    ask = scrapy.Field()  # 提问
    answer = scrapy.Field()  # 回答
    articles = scrapy.Field()  # 文章
    avatar_url = scrapy.Field()  # 头像url
    main_page_url = scrapy.Field()  # 主页
    avatar_local_url = scrapy.Field()  # 本机位置
    id = scrapy.Field()
    images = scrapy.Field()


class ZhihuFollowee(scrapy.Item):
    follow_id = scrapy.Field() #表示谁关注的
    id = scrapy.Field()  # uid
    gender = scrapy.Field()  # 性别
    name = scrapy.Field()  # 用户名
    url_token = scrapy.Field()  # 用户地址末段链接
    user_type = scrapy.Field()  # 用户类型
    is_advertiser = scrapy.Field()  # 是否是广告者
    avatar_url = scrapy.Field()  # 用户头像url
    is_org = scrapy.Field() #是否是组织
    # headline = scrapy.Field() # 简介
    avatar_local_url = scrapy.Field()  # 本机位置
    main_page_url=scrapy.Field() # 主页URL