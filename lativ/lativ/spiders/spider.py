import scrapy
from lativ.items import LativItem

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

class LativSpider(scrapy.Spider):

    name = 'lativ'
    # allowed_domains = ['lativ.com']
    start_urls = [
        # 'http://www.lativ.com/MEN'
        'http://t.bookdna.cn/'
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

        for sel in response.css('.container > div'):

            item = LativItem()
            item['name'] = sel.css('b::text').extract_first().strip()
            item['lowest_price'] = sel.css('div > div > span::text').extract_first().strip()
            item['current_price'] = sel.css('div > span > span::text').extract_first().strip()
            item['content'] = sel.css('div > div::text').extract_first().strip()
            print sel.xpath('text()').extract_first().encode('utf8')
            yield item

            print "\n"





