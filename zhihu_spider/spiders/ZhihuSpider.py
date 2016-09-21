#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by dengqiangxi on 16/9/12
import scrapy
from scrapy.http import Request
from zhihu_spider.settings import *
from zhihu_spider.items import ZhihuSpiderItem
import hashlib
import re


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    start_urls = ['https://www.zhihu.com/people/chi-chu-63']
    allowed_domains = ['www.zhihu.com']

    def __init__(self, **kwargs):
        super(ZhihuSpider, self).__init__(**kwargs)
        self.base_url = 'https://www.zhihu.com'
        self.followees_url = 'https://www.zhihu.com/node/ProfileFolloweesListV2'

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return Request(url, method='GET',headers=ZHIHU_HEADER, cookies=ZHIHU_COOKIE)

    def parse(self, response):
        item = ZhihuSpiderItem()
        user_name = response.css('.title-section .name::text').extract_first()
        print user_name
        if user_name:
            item['user_name'] = user_name
        follow = response.css(
            'body > div.zg-wrap.zu-main.clearfix > div.zu-main-sidebar > div.zm-profile-side-following.zg-clear > a> strong::text').extract()

        if follow:
            if follow[0]:
                item['followees'] = int(follow[0])
            if follow[1]:
                item['followers'] = int(follow[1])

        item['introduce'] = ''.join(response.css(
            'div.zg-wrap.zu-main.clearfix > div.zu-main-content > div > div.zm-profile-header.ProfileCard > div.zm-profile-header-main > div > div.zm-profile-header-info > div > div.zm-profile-header-description.editable-group > span.info-wrap.fold-wrap.fold.disable-fold > span.fold-item > span::text').extract())
        item['ellipsis'] = ''.join(response.css(
            'body > div.zg-wrap.zu-main.clearfix > div.zu-main-content > div > div.zm-profile-header.ProfileCard > div.zm-profile-header-main > div > div.top > div.title-section > div::text').extract())

        item['location'] = ''.join(response.css('.location .topic-link::text').extract())

        item['major'] = ''.join(response.css('.business .topic-link::text').extract())

        head_url = re.sub(r'_l\.', '.', ''.join(response.css('.body .Avatar--l::attr(src)').extract()))
        arr = []
        arr.append(head_url)
        item['head_image'] = head_url
        item['image_urls'] = arr
        item['ask'] = int(''.join(response.css('.active+ .item .num::text').extract()))

        item['answer'] = int(''.join(response.css('.item:nth-child(3) .num::text').extract()))

        item['articles'] = int(''.join(response.css('.item:nth-child(4) .num::text').extract()))

        item['collected'] = int(''.join(response.css('.item:nth-child(5) .num::text').extract()))

        item['public_editor'] = int(''.join(response.css('.item:nth-child(6) .num::text').extract()))

        item['views'] = int(''.join(response.css('.zg-gray-normal strong::text').extract()))

        if response.url:
            item['main_page'] = response.url
        print response.url
        item['_id'] = hashlib.sha1(response.url).hexdigest()
        yield item

        urls = response.css(
            'body > div.zg-wrap.zu-main.clearfix > div.zu-main-sidebar > div.zm-profile-side-following.zg-clear > a:nth-child(1)::attr(href)').extract()

        if urls:
            for url in urls:
                url = 'https://www.zhihu.com' + url
                yield scrapy.Request(url=url, callback=self.parse_followers,headers=ZHIHU_HEADER, cookies=ZHIHU_COOKIE)

    def parse_followers(self, response):
        urls = response.xpath('//*[@id="zh-profile-follows-list"]/div/div/a/@href').extract()
        if urls:
            for url in urls:
                url = self.base_url + url
                yield scrapy.Request(url=url, callback=self.parse,headers=ZHIHU_HEADER, cookies=ZHIHU_COOKIE)