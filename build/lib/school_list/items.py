# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SchoolListItem(Item):
    _id = Field()
    name = Field()
    desc = Field()
    icon = Field()
    area = Field()
    address = Field()
    tell = Field()
    type = Field()
    attr = Field()
    nature = Field()
    url = Field()
    score = Field()
    comment = Field()
    score_count = Field()
    province = Field()
