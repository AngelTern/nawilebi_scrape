# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NawilebiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    website = scrapy.Field()
    part_url = scrapy.Field()
    car_mark = scrapy.Field()
    part_full_name = scrapy.Field()
    car_model = scrapy.Field()
    year = scrapy.Field()
    #oem = scrapy.Field()
    price = scrapy.Field()
    in_stock = scrapy.Field()
    city = scrapy.Field()
    pass
