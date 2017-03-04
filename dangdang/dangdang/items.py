# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SessionItem(scrapy.Item):
    # name = scrapy.Field()

    session_online_id = scrapy.Field()
    session_name      = scrapy.Field()
    session_img_url   = scrapy.Field()
    session_rest_day  = scrapy.Field()
    session_msg       = scrapy.Field()
    session_url       = scrapy.Field()

    pass

class BookItem(scrapy.Item):

    book_online_id     = scrapy.Field()
    book_name          = scrapy.Field()
    book_orignal_price = scrapy.Field()
    book_current_price = scrapy.Field()
    book_lowest_price  = scrapy.Field()
    book_img_url       = scrapy.Field()
    book_pubuliser     = scrapy.Field()
    book_from          = scrapy.Field()
    book_rating_people = scrapy.Field()
    book_rating_point  = scrapy.Field()
    book_writer        = scrapy.Field()
    book_page_url      = scrapy.Field()
    book_disable       = scrapy.Field()
    book_keywords      = scrapy.Field()
