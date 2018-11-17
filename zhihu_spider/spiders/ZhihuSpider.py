#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by dengqiangxi on 16/9/12
import logging

import scrapy
from scrapy.http import Request, Response
from zhihu_spider.settings import *
from zhihu_spider.items import *
from zhihu_spider.misc.db_tools import *
import json

from zhihu_spider.misc.tools import config_logger

config_logger()

ignore_key_set = {'isFollowed', 'vipInfo', 'accountStatus', 'messageThreadToken', 'isFollowing', 'orgHomepage',
                  'industryCategory'}


def parse_sub_item(sub_item_obj: dict, sub_item: Item):
    for sub_key, sub_value in sub_item_obj.items():
        if sub_key in Employment.fields.keys():
            if sub_key == 'meta':
                sub_item[sub_key] = json.dumps(sub_value, ensure_ascii=False)
            else:
                sub_item[sub_key] = sub_value


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    type_format_str = '''https://www.zhihu.com/api/v4/members/{}/{}?limit=20&offset=100'''
    # type_format_str = '''https://www.zhihu.com/api/v4/members/{}/{}?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&limit=20&offset=0'''
    url_user_info_api_format = 'https://api.zhihu.com/people/{}'
    start_urls = [
        url_user_info_api_format.format('0970f947b898ecc0ec035f9126dd4e08'),
        url_user_info_api_format.format('80d73b7ec52adc8afd54894cead6063f'),
        url_user_info_api_format.format('8b68876001197b3b9cd605b20814616f'),
    ]

    def __init__(self, **kwargs):
        super(ZhihuSpider, self).__init__(**kwargs)
        self.base_url = 'https://www.zhihu.com'
        self.following_url = 'https://www.zhihu.com/people/renfish/following'

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return Request(url, method='GET', headers=ZHIHU_HEADER)

    def parse(self, response: Response):
        """
        解析单个用户的详细信息
        :param response:
        """
        text = response.text
        user_info = json.loads(text)
        raw_data_obj = RawDataItem()
        raw_data_obj['json_obj'] = user_info
        yield raw_data_obj
        item = UserInfo()
        for key, value in user_info.items():
            if key in ignore_key_set:
                continue
            if key == 'vipInfo':
                item['isVip'] = value.get('isVip')
            elif key == 'education':
                edu_names = []
                for e_item in value:
                    if not e_item:
                        continue
                    education_item = Education()
                    parse_sub_item(e_item, education_item)
                    if education_item['name'] not in db_education_names:
                        db_education_names.add(education_item['name'])
                        yield education_item
                    edu_names.append(e_item['name'])
                item[key] = json.dumps(edu_names, ensure_ascii=False)
            elif key == 'employment':
                all_employ_names = []
                for e_item in value:
                    employ_names = []
                    for e_sub_item in e_item:
                        if not e_sub_item:
                            continue
                        employ_item = Employment()
                        parse_sub_item(e_sub_item, employ_item)
                        if employ_item['name'] not in db_employ_names:
                            db_employ_names.add(employ_item['name'])
                            yield employ_item
                        employ_names.append(e_sub_item['name'])
                    all_employ_names.append(employ_names)

                item[key] = json.dumps(all_employ_names, ensure_ascii=False)
            elif key == 'location':
                location_names = []
                for l_item in value:
                    if not l_item:
                        continue
                    location = Location()
                    parse_sub_item(l_item, location)
                    l_name = l_item.get('name')
                    location_names.append(l_name)
                    if l_name not in db_location_names:
                        db_location_names.add(l_name)
                        yield location
                item[key] = json.dumps(location_names, ensure_ascii=False)
            elif key == 'business':
                business_item = Business()
                if not value:
                    continue
                parse_sub_item(value, business_item)
                b_name = value.get('name')
                item[key] = b_name
                if b_name not in db_business_names:
                    db_business_names.add(b_name)
                    yield business_item
            elif key == 'badge':
                badge_items = []
                for badge_item in value:
                    topics = badge_item.get('topics')
                    if topics:
                        topic_names = []
                        for topic_item in topics:
                            if not topic_item:
                                continue
                            topic = Topic()
                            parse_sub_item(topic_item, topic)
                            topic_names.append(topic_item.get('name'))
                            if topic['name'] not in db_topic_names:
                                db_topic_names.add(topic['name'])
                                yield topic
                        del badge_item['topics']
                        badge_item['topic_names'] = topic_names
                    badge_items.append(badge_item)
                item[key] = json.dumps(badge_items, ensure_ascii=False)
            elif key == 'infinity':
                item[key] = json.dumps(value, ensure_ascii=Field)
            else:
                if key in UserInfo.fields.keys():
                    item[key] = value
        db_user_ids.add(item['id'])
        yield item
        url_token = item['url_token']
        api_followings_url = self.type_format_str.format(url_token, 'followees')
        api_followers_url = self.type_format_str.format(url_token, 'followers')

        yield scrapy.Request(url=api_followings_url, callback=self.parser_follow_json, headers=ZHIHU_HEADER,
                             meta={'url_token': url_token})
        yield scrapy.Request(url=api_followers_url, callback=self.parser_follow_json, headers=ZHIHU_HEADER,
                             meta={'url_token': url_token})

    def parser_follow_json(self, response):
        """
        从粉丝和关注者的接口中抽出用户的token
        """
        url_token = response.meta['url_token']
        json_text = response.text
        f_obj = json.loads(json_text)
        paging = f_obj['paging']
        data = f_obj['data']
        item = {}
        if 'followers' in response.url:
            item = Follower()
        elif 'followees' in response.url or 'following' in response.url:
            item = Following()
        if data:
            for userinfo in data:
                if isinstance(item, Following):
                    item['follower_token'] = url_token
                    item['following_token'] = userinfo['url_token']
                else:
                    item['follower_token'] = userinfo['url_token']
                    item['following_token'] = url_token
                yield item
                user_id = userinfo['url'].split('/')[-1]
                if user_id not in db_user_ids:
                    logging.info("%s not in ids", user_id)
                    db_user_ids.add(user_id)
                    json_url = self.url_user_info_api_format.format(user_id)
                    yield scrapy.Request(url=json_url,
                                         callback=self.parse,
                                         headers=ZHIHU_HEADER)

        if paging and not paging['is_end']:
            next_url = paging['next'].replace('https://www.zhihu.com', 'https://www.zhihu.com/api/v4')
            print('next_url', next_url)
            yield scrapy.Request(url=next_url, callback=self.parser_follow_json, headers=ZHIHU_HEADER,
                                 dont_filter=True, meta={'url_token': url_token})
