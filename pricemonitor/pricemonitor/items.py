# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PricemonitorItem(scrapy.Item):
    # define the fields for your item here like:
    store = scrapy.Field()
    brand = scrapy.Field()
    product = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    url = scrapy.Field()
    scraped_at = scrapy.Field()
