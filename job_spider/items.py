# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class JobSpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    provider = Field()
    id = Field()
    title = Field()
    company = Field()
    url = Field()
    techs = Field()
    dt_posted = Field()
    dt_pulled = Field()

    pass