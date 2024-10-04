# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class FightInfoItem(scrapy.Item):
    event_name_info = scrapy.Field()
    fighter_1_name_info = scrapy.Field()
    fighter_2_name_info = scrapy.Field()
    result_info = scrapy.Field()
    method_info = scrapy.Field()
    event_date_info = scrapy.Field()

class EventItem(scrapy.Item):
    event_name = scrapy.Field()
    event_data = scrapy.Field()

class FighterItem(scrapy.Item):
    name = scrapy.Field()
    elo_rating = scrapy.Field()

class FightItem(scrapy.Item):
    fighter_1_id = scrapy.Field()
    fighter_2_id = scrapy.Field()
    result = scrapy.Field()
    method = scrapy.Field()
    event_id = scrapy.Field()