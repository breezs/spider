# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    positionInfo = scrapy.Field()
    model= scrapy.Field()
    area= scrapy.Field()
    direction= scrapy.Field()
    zhuangxiu= scrapy.Field()
    floor= scrapy.Field()
    create_time= scrapy.Field()
    floor_type= scrapy.Field()
    totalPrice=scrapy.Field()
    unitPrice=scrapy.Field()
