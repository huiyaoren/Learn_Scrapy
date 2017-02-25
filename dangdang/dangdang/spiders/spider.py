import scrapy
from dangdang.items import BookItem, SessionItem

class DangdangSpider(scrapy.Spider):

    name = 'dangdang'
    start_urls = [
        'http://v.dangdang.com/book'
    ]

    def parse(self, response):

        item = SessionItem()
        for sel in response.css('ul.list_aa > li > a'):
            item['session_url'] =  sel.css('a::attr(href)').extract_first().strip()
            item['session_msg'] =  sel.css('.price_s > span::text').extract_first().strip()
            item['session_msg'] =  sel.css('.price_s::text').extract_first().strip()
            item['session_img_url'] =  sel.css('.little_logo > img::attr(data-original)').extract_first().strip()
            item['session_name'] =  sel.css('a::attr(title)').extract_first().strip()
            # item['session_rest_day'] =  sel.css('.sale_time > span > span > span::text').extract_first().strip()
            item['session_online_id'] = int(item['session_url'].split('_')[-2])

            yield item

