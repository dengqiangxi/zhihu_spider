# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from .misc.all_secret_set import mysql_config
import random
from .misc.user_agents import user_agent_list
import pymysql
from zhihu_spider.items import ZhihuSpiderItem, ZhihuFollowee
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline, FileException
from scrapy.http import Request


class ZhihuImagePipeLine(ImagesPipeline):
    def get_media_requests(self, item, info):
        print('下载图片')
        yield Request(url=item['avatar_url'], headers={
            "Referer": item['main_page_url'],
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        })

    def item_completed(self, results, item, info):
        # print(results)
        if results and results[0] and results[0][0]:
            item['avatar_local_url'] = results[0][1]['path']
        # print(item)
        return item


class ZhihuSpiderPipeLine(object):
    def __init__(self):
        self.connection = pymysql.connect(**mysql_config)
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        if isinstance(item, ZhihuSpiderItem):
            self.saveOrUpdateUserInfo(item)
        if isinstance(item, ZhihuFollowee):
            self.saveOrUpdateFollowees(item)

    def saveOrUpdateUserInfo(self, item):
        try:
            id = item['id']
            sql_select_id = 'SELECT id FROM zh_userinfo WHERE id="' + id + '"'
            sql_insert_content = 'INSERT INTO zh_userinfo (id, name, followees, followers, detail_introduce, major, ask, answer, articles, avatar_url, main_page_url) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' \
                                 % (
                                     id, item['name'], item['followees'], item['followers'],
                                     item['detail_introduce'], item['major'], item['ask'], item['answer'],
                                     item['articles'],
                                     item['avatar_url'], item['main_page_url'])
            sql_update_content = 'UPDATE zh_userinfo SET followees="%s",followers="%s",detail_introduce="%s",major="%s",ask="%s",answer="%s",articles="%s" WHERE id="%s"' % (
                item['followees'], item['followers'],
                item['detail_introduce'], item['major'], item['ask'], item['answer'],
                item['articles'], id
            )
            self.cursor.execute(sql_select_id)
            # print(user_select)
            if not self.cursor.fetchone():
                print('sql_insert_content', sql_insert_content)
                self.cursor.execute(sql_insert_content)
            else:
                print('sql_update_content', sql_update_content)
                self.cursor.execute(sql_update_content)
            self.connection.commit()
            return item
        except:
            self.connection.rollback()
            raise DropItem('重复喽')

    def saveOrUpdateFollowees(self, item):
        try:
            follow_id = item['follow_id']
            id = item['id']
            sql_selector_user = 'SELECT id FROM zh_userinfo WHERE id="%s"' % (id)
            # sql_insert_user = 'INSERT INTO zh_friend (uid, fid, name) VALUES ("%s","%s","%s") ON DUPLICATE '
            sql_insert_user = 'INSERT INTO zh_userinfo (id, name, gender, avatar_url, main_page_url) VALUES ("%s","%s","%s","%s","%s") ' % (
                id, item['name'], item['gender'], item['avatar_url'], item['main_page_url'])
            print(sql_insert_user)
            self.cursor.execute(sql_selector_user)
            if not self.cursor.fetchall():
                self.cursor.execute(sql_insert_user)
            sql_select_fid = 'SELECT * FROM zh_friend WHERE uid="%s" AND fid="%s"' % (follow_id, id)
            sql_insert_friends = 'INSERT INTO zh_friend (uid, fid,name) VALUES ("%s","%s","%s")' % (follow_id, id,item['name'])
            self.cursor.execute(sql_select_fid)
            p = self.cursor.fetchall()
            print('获取all',p)
            if not p:
                print('sql_insert_friends',sql_insert_friends)
                self.cursor.execute(sql_insert_friends)
            self.connection.commit()
            return item
        except:
            self.connection.rollback()
            raise DropItem('重复喽')
