# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class EventItem(scrapy.Item):
    event_name = scrapy.Field()

class FighterItem(scrapy.Item):
    name = scrapy.Field()
    elo_rating = scrapy.Field()

class FightItem(scrapy.Item):
    fighter_1_id = scrapy.Field()
    fighter_2_id = scrapy.Field()
    result = scrapy.Field()
    method = scrapy.Field()
    event_id = scrapy.Field()