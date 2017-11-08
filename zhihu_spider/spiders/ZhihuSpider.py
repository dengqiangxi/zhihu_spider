#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by dengqiangxi on 16/9/12
import scrapy
from scrapy.http import Request
from zhihu_spider.settings import *
from zhihu_spider.misc.all_secret_set import ZHIHU_COOKIE
from zhihu_spider.items import ZhihuSpiderItem, ZhihuFollowee
from zhihu_spider.misc.tools import getId
import re, json


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'

    start_urls = ['https://www.zhihu.com/people/chi-chu-63']
    allowed_domains = ['www.zhihu.com']

    def __init__(self, **kwargs):
        super(ZhihuSpider, self).__init__(**kwargs)
        self.base_url = 'https://www.zhihu.com'
        self.followees_url = 'https://www.zhihu.com/people/renfish/following'
        self.re_views = re.compile('\d*')

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return Request(url, method='GET', headers=ZHIHU_HEADER, cookies=ZHIHU_COOKIE)

    def parse(self, response):
        item = ZhihuSpiderItem()
        # item = {}
        user_name = response.css('span[class="ProfileHeader-name"]::text').extract_first()

        if response.url:
            item['main_page_url'] = response.url

        if user_name:
            item['name'] = user_name
        follow = response.css(
            'div[class="Card FollowshipCard"]>div>a>div[class="NumberBoard-value"]::text').extract()

        if follow:
            if follow[0]:
                item['followees'] = int(follow[0])
            if follow[1]:
                item['followers'] = int(follow[1])

                # thanks_support = response.css('div[class="IconGraf"] div[class="IconGraf-iconWrapper"]::text').extract()

                # if thanks_support:
                #     for t in thanks_support:
                # print(t)

        # item['headline'] = response.css('span[class="RichText ProfileHeader-headline"]::text').extract_first()
        item['detail_introduce'] = ''.join(response.css(
            ' div[class="RichText ProfileHeader-detailValue"]::text').extract())

        item['location'] = ''.join(response.css('.location .topic-link::text').extract())

        item['major'] = response.css('div[class="ProfileHeader-infoItem"]::text').extract_first()

        head_img_url = response.css('img[class="Avatar Avatar--large UserAvatar-inner"]::attr(src)').extract_first()

        item['avatar_url'] = head_img_url
        item['ask'] = int(
            response.css('li[aria-controls="Profile-asks"]>a>span[class="Tabs-meta"]::text').extract_first())

        item['answer'] = int(
            response.css('li[aria-controls="Profile-answers"]>a>span[class="Tabs-meta"]::text').extract_first())

        item['articles'] = int(
            response.css('li[aria-controls="Profile-posts"]>a>span[class="Tabs-meta"]::text').extract_first())

        item['id'] = getId(response.url)
        # print(item)


        url = response.css(
            'div[class="Card FollowshipCard"]>div>a[class="Button NumberBoard-item Button--plain"]::attr(href)').extract_first()
        yield item
        if url:
            url = self.base_url + url
            yield scrapy.Request(url=url, callback=self.parse_followers, headers=ZHIHU_HEADER, cookies=ZHIHU_COOKIE,
                                 meta={
                                     'uid': item['id']
                                 })

    def parse_followers(self, response):
        uid = response.meta['uid']
        api_url = self.base_url + '/api/v4/members/' + response.url.split('/')[-2] + '/followees'

        yield scrapy.Request(url=api_url, callback=self.parser_follower_json, headers=ZHIHU_HEADER,
                             cookies=ZHIHU_COOKIE, dont_filter=True, meta={
                'uid': uid
            })
    # 解析json
    def parser_follower_json(self, response):
        follow_id = response.meta['uid']
        json_text = response.text
        followees_obj = json.loads(json_text)
        paging = followees_obj['paging']
        data = followees_obj['data']

        if data:
            for userinfo in data:
                followee_item = ZhihuFollowee()

                user_url = self.base_url + '/people/' + userinfo['url_token']  # 拼接成用户个人网址
                followee_item['follow_id'] = follow_id
                followee_item['id'] = getId(user_url)
                followee_item['gender'] = userinfo['gender']
                followee_item['name'] = userinfo['name']
                followee_item['url_token'] = userinfo['url_token']
                followee_item['user_type'] = userinfo['user_type']
                followee_item['is_advertiser'] = userinfo['is_advertiser']
                followee_item['avatar_url'] = userinfo['avatar_url']
                followee_item['is_org'] = userinfo['is_org']
                # followee_item['headline'] = userinfo['headline'][:60]
                followee_item['main_page_url'] = user_url
                yield followee_item

                yield scrapy.Request(url=user_url, callback=self.parse, headers=ZHIHU_HEADER, cookies=ZHIHU_COOKIE)

        if paging and not paging['is_end']:
            next_url = paging['next'].replace('http://', 'https://')
            yield scrapy.Request(url=next_url, callback=self.parser_follower_json, headers=ZHIHU_HEADER,
                                 cookies=ZHIHU_COOKIE, dont_filter=True, meta={
                    'uid': follow_id
                })