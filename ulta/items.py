# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UltaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand = scrapy.Field()
    product = scrapy.Field()
    price = scrapy.Field()
    details = scrapy.Field()
    reviews = scrapy.Field()
    rating = scrapy.Field()
    categories = scrapy.Field()
    size = scrapy.Field()
