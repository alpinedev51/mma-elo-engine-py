# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class FightItem(scrapy.Item):
    # define the fields for your item here like:
    event_name = scrapy.Field()
    fighter_1 = scrapy.Field()
    fighter_2 = scrapy.Field()
    result = scrapy.Field()
    method = scrapy.Field()
