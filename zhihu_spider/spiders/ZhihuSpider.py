#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by dengqiangxi on 16/9/12
import scrapy
from scrapy.http import Request
from zhihu_spider.settings import *
from zhihu_spider.misc.all_secret_set import ZHIHU_COOKIE
from zhihu_spider.items import ZhihuSpiderItem, ZhihuFollowee,ZhihuFollower
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
        headline =response.css('span[class="RichText ProfileHeader-headline"]::text').extract_first()
        item['headline'] = headline.replace('"',"'")  if headline else "None"
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

        item['nametoken'] = response.url.split('/')[-1]


        url = response.css(
            'div[class="Card FollowshipCard"]>div>a[class="Button NumberBoard-item Button--plain"]::attr(href)').extract_first()
        yield item
        # print(item)
        if url:
            url = self.base_url + url
            yield scrapy.Request(url=url, callback=self.parse_followers, headers=ZHIHU_HEADER, cookies=ZHIHU_COOKIE,
                                 meta={
                                     'nametoken': item['nametoken']
                                 })

    def parse_followers(self, response):
        nametoken = response.meta['nametoken']
        api_followees_url = self.base_url + '/api/v4/members/' + response.url.split('/')[-2] + '/followees'
        api_followers_url = self.base_url + '/api/v4/members/' + response.url.split('/')[-2] + '/followers'

        yield scrapy.Request(url=api_followees_url, callback=self.parser_follow_json, headers=ZHIHU_HEADER,
                             cookies=ZHIHU_COOKIE, meta={
                'nametoken': nametoken
            })
        yield scrapy.Request(url=api_followers_url, callback=self.parser_follow_json, headers=ZHIHU_HEADER,
                             cookies=ZHIHU_COOKIE, meta={
                'nametoken': nametoken
            })




    # 解析json
    def parser_follow_json(self, response):
        nametoken = response.meta['nametoken']
        json_text = response.text
        print(json_text)
        f_obj = json.loads(json_text)
        paging = f_obj['paging']
        data = f_obj['data']
        print('23333',response.url.find('followers'))
        item={}
        if response.url.find('followers')>0:
            item =ZhihuFollower()
        elif response.url.find('followees')>0:
            item=ZhihuFollowee()
        if data:
            for userinfo in data:
                user_url = self.base_url + '/people/' + userinfo['url_token']  # 拼接成用户个人网址
                item['ftoken'] = nametoken
                item['gender'] = userinfo['gender']
                item['name'] = userinfo['name']
                item['nametoken'] = userinfo['url_token']
                item['user_type'] = userinfo['user_type']
                item['is_advertiser'] = userinfo['is_advertiser']
                item['avatar_url'] = userinfo['avatar_url']
                item['is_org'] = userinfo['is_org']
                head_line = userinfo['headline']
                item['headline'] = head_line.replace('"', "'") if head_line else 'None'
                item['main_page_url'] = user_url
                yield item
                yield scrapy.Request(url=user_url, callback=self.parse, headers=ZHIHU_HEADER, cookies=ZHIHU_COOKIE)

        if paging and not paging['is_end']:
            next_url = paging['next'].replace('http://', 'https://')
            yield scrapy.Request(url=next_url, callback=self.parser_follow_json, headers=ZHIHU_HEADER,
                                 cookies=ZHIHU_COOKIE, dont_filter=True, meta={
                    'nametoken': nametoken
                })


