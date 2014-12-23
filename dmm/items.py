# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy.item import Item,Field

class DmmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id=scrapy.Field()
    video_code=scrapy.Field()
    video_title=scrapy.Field()
    sale_date=scrapy.Field()
    video_actor=scrapy.Field()
    video_time=scrapy.Field()
    video_series=scrapy.Field()#系列
    video_level=scrapy.Field()#级别
    video_genre=scrapy.Field()#分类
    video_company=scrapy.Field()#公司
    thumb_url=scrapy.Field()
    video_thumb=scrapy.Field()#缩略图
    pic_url=scrapy.Field()
    video_pic=scrapy.Field()#照片

class ActorItem(scrapy.Item):
    _id=scrapy.Field()
    actor_code=scrapy.Field()
    actor_name=scrapy.Field()

class SeriesItem(scrapy.Item):
    _id=scrapy.Field()
    series_code=scrapy.Field()
    series_name=scrapy.Field()

class GenreItem(scrapy.Item):
     _id=scrapy.Field()
     genre_code=scrapy.Field()
     genre_name=scrapy.Field()

class CompanyItem(scrapy.Item):
    _id=scrapy.Field()
    company_code=scrapy.Field()
    company_name=scrapy.Field()

class VideoItem(scrapy.Item):
    _id=scrapy.Field()
    video_code=scrapy.Field()
    video_actor=scrapy.Field()

class LevelItem(scrapy.Item):
    _id=scrapy.Field()
    level_code=scrapy.Field()
    level_name=scrapy.Field()


    pass


