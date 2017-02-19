import scrapy
from lativ.items import LativItem

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

class LativSpider(scrapy.Spider):

    name = 'lativ'
    allowed_domains = ['lativ.com']
    start_urls = [
        'http://www.lativ.com/OnSale/down/MEN'
    ]

    # def output(func):
    #     def wrap(func):
    #         print "=======================================================\n"
    #         func()
    #         print "=======================================================\n"
    #     return wrap
    #
    # @output
    def parse(self, response):

        # item = LativItem()
        # item['content'] = response.xpath('//h1/text()').extract()
        # return [item]


        for sel in response.css('li'):

            item = LativItem()
            item['content'] = sel.xpath('text()').extract_first().strip()
            print sel.xpath('text()').extract_first().encode('utf8')
            yield item

            print "\n"





