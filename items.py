# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class SpiderCodeItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()


class BeianItem(scrapy.Item):
    """备案信息"""
    企业名称 = scrapy.Field()
    统一社会信用代码 = scrapy.Field()
    企业链接地址 = scrapy.Field()
    企业类型 = scrapy.Field()
    企业营业地址 = scrapy.Field()
    注册地址 = scrapy.Field()
    采集来源省 = scrapy.Field()
    省内或省外 = scrapy.Field()
    登记状态 = scrapy.Field()
    所属地区 = scrapy.Field()
    来源网站 = scrapy.Field()
    网站代码 = scrapy.Field()
    属地类别 = scrapy.Field()

    信息登记编号 = scrapy.Field()
    企业法定代表人 = scrapy.Field()
    进冀负责人 = scrapy.Field()
    驻鄂机构所在地市州 = scrapy.Field()
    备注 = scrapy.Field()
    md5 = scrapy.Field()


class AutoItem(scrapy.Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = Field()
        self._values[key] = value
