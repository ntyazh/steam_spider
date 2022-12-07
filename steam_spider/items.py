# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamSpiderItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    reviews_amount = scrapy.Field()
    general_score = scrapy.Field()
    release_date = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()

