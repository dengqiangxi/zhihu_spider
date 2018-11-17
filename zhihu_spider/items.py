# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class UserInfo(Item):
    education = Field()
    following_count = Field()
    vote_from_count = Field()
    user_type = Field()
    included_text = Field()
    pins_count = Field()
    is_privacy_protected = Field()
    included_articles_count = Field()
    is_force_renamed = Field()
    id = Field()
    favorite_count = Field()
    voteup_count = Field()
    commercial_question_count = Field()
    is_blocking = Field()
    following_columns_count = Field()
    headline = Field()
    url_token = Field()
    participated_live_count = Field()
    is_advertiser = Field()
    following_favlists_count = Field()
    favorited_count = Field()
    is_org = Field()
    follower_count = Field()
    employment = Field()
    type = Field()
    avatar_hue = Field()
    avatar_url_template = Field()
    following_topiceducation_count = Field()
    description = Field()
    business = Field()
    avatar_url = Field()
    columns_count = Field()
    hosted_live_count = Field()
    is_active = Field()
    thank_to_count = Field()
    mutual_followees_count = Field()
    cover_url = Field()
    thank_from_count = Field()
    vote_to_count = Field()
    is_blocked = Field()
    answer_count = Field()
    allow_message = Field()
    articles_count = Field()
    name = Field()
    question_count = Field()
    location = Field()
    badge = Field()
    included_answers_count = Field()
    url = Field()
    logs_count = Field()
    following_question_count = Field()
    thanked_count = Field()
    gender = Field()

    sina_weibo_url = Field()
    sina_weibo_name = Field()
    marked_answers_text = Field()

    shared_count = Field()
    lite_favorite_content_count = Field()
    independent_articles_count = Field()
    reactions_count = Field()
    is_activity_blocked = Field()
    is_bind_sina = Field()
    is_hanged = Field()
    is_unicom_free = Field()
    live_count = Field()
    is_baned = Field()
    is_enable_signalment = Field()
    is_enable_watermark = Field()
    infinity = Field()


class Base(Item):
    url = Field()
    avatar_url = Field()
    name = Field()
    introduction = Field()
    type = Field()
    excerpt = Field()
    id = Field()
    meta = Field()


class Business(Base):
    experience = Field()
    pass


class Location(Base):
    pass


class Topic(Base):
    pass


class Education(Base):
    pass


class Employment(Base):
    pass


class Following(Item):
    follower_token = Field()
    following_token = Field()


#    is_vip 需要转换


class Follower(Item):
    follower_token = Field()
    following_token = Field()


class RawDataItem(Item):
    json_obj = Field()


class TestLoader(ItemLoader):
    default_item_class = UserInfo
    default_input_processor = TakeFirst()
