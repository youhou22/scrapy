# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianqiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    day = scrapy.Field()  # 日期
    weatherm = scrapy.Field()  # 白天天气
    weathern = scrapy.Field()  # 晚上天气
    temm = scrapy.Field()  # 白天温度
    temn = scrapy.Field()  # 晚上温度
    windm = scrapy.Field()  # 白天风向
    windn = scrapy.Field()  # 晚上风向

