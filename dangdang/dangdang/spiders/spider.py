# coding: utf8
import json

import scrapy
from dangdang.items import BookItem, SessionItem
from scrapy import FormRequest
from scrapy import Request


class DangdangSpider(scrapy.Spider):

    name = 'dangdang'
    start_urls = [
        'http://v.dangdang.com/book'
    ]


    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

        # return [FormRequest("http://pubs.rsc.org/en/search/journalresult",
        #                     formdata={'resultcount': '100', 'category': 'all', 'pageno': '1'},
        #                     callback=self.parse)]

        # pages=[]
        # for i in range(1,10):
        #     url='http://www.example.com/?page=%s'%i
        #     page=scrapy.Request(url)
        #     pages.append(page)
        # return pages

    def parse(self, response):
        item = SessionItem()
        for sel in response.css('ul.list_aa > li > a'):
            item['session_url'] = sel.css('a::attr(href)').extract_first().strip()
            item['session_msg'] = sel.css('.price_s > span::text').extract_first().strip()
            item['session_msg'] = sel.css('.price_s::text').extract_first().strip()
            item['session_img_url'] = sel.css('.little_logo > img::attr(data-original)').extract_first().strip()
            item['session_name'] = sel.css('a::attr(title)').extract_first().strip()
            # item['session_rest_day'] = sel.css('.sale_time > span > span > span::text').extract_first().strip()
            item['session_online_id'] = int(item['session_url'].split('_')[-2])

            yield item


class TestSpider(scrapy.Spider):

    name = 'test'

    def start_requests(self):
        return [FormRequest("http://localhost/bsdapp/api/user/register_post",
                                formdata={
                                    'user_name':      'beston4',
                                    'user_password':  '1231b2f3 ',
                                    'user_sex':       '男',
                                    'user_age':       '21',
                                    'user_phone':     '2311333433',
                                    'user_mail':      '1113@462.com'
                                }
                            )]
        #
        # return [Request("http://localhost/bsdapp/api/user/register_post",
        #                 method='POST',
        #                 body="user_name='beston3'&user_password='123123'&user_sex='男'&user_age=1&user_phone=11131311121&user_mail='ws23@26.com'",
        #                 )]



    def parse(self, response):
        print("++++++++++++++++++++++++++++++++++++++")
        print(response.text)
        print(type(response.text))

        try:
            a = json.loads(response.body_as_unicode())
        except:
            a = response.text

        print(a)
        print(type(a))

        try:
            print(a['error']['warning'])
            print(a['error']['data'])
            print(a['error']['sql'])
        except:
            print(u'无错误信息')
        print("++++++++++++++++++++++++++++++++++++++")


