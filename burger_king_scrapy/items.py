# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BurgerKingScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    brand_name = scrapy.Field()
    # State & city
    state_name = scrapy.Field()
    city_name = scrapy.Field()
    city_link = scrapy.Field()

    # Store details
    address = scrapy.Field()
    pincode = scrapy.Field()
    phone_number = scrapy.Field()
    time = scrapy.Field()

    # URLs
    website = scrapy.Field()
    map = scrapy.Field()

    # discription = scrapy.Field()
    region = scrapy.Field()
    delivery_time = scrapy.Field()
    cost = scrapy.Field()

    good_for = scrapy.Field()


