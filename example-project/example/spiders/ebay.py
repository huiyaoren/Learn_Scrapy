# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider
from example.items import CategoryItem, ProductItem, ExampleLoader
from redis import Redis


class EbaySpider(Spider):
    name = 'ebay'
    allowed_domains = ['ebay.com']
    start_urls = ['http://www.ebay.com/sch/allcategories/all-categories']

    def parse(self, response):

        datas = response.xpath("//div[@class='gcma']/ul/li/a[@class='ch']")
        for data in datas:
            try:
                item = CategoryItem()
                item['name'] = data.xpath("text()").extract_first()
                item['link'] = data.xpath("@href").extract_first()
                yield item
                # redis.lpush()
            except():
                print('===== Something Wrong =====')


class DangSpider(RedisCrawlSpider):
    name = 'dang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://v.dangdang.com/book']
    redis_key = 'dang:start_urls'
    settings = get_project_settings()

    book_session_lx = LinkExtractor(allow=(r'http://v.dangdang.com/book',))
    book_list_lx = LinkExtractor(allow=(r'http://v.dangdang.com/pn0_\d+_\d+.html',))
    # boot_item_lx = LinkExtractor(allow=(r'http://product.dangdang.com/\d+.html',))

    rules = (
        Rule(book_session_lx, callback='parse_book_session'),
        Rule(book_list_lx, callback='parse_book_list')
    )

    def __init__(self, *args, **kwargs):
        # 初始化的意义 ?：
        # 动态定义 allowed_domains 列表
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(DangSpider, self).__init__(*args, **kwargs)

    def parse_book_session(self, response):
        datas = response.xpath("//div[@class='col left']/div/div/ul/li/a")
        for data in datas:
            try:
                item = CategoryItem()
                item['name'] = data.xpath("span[@class='shop_name']/text()").extract_first()
                item['link'] = data.xpath("@href").extract_first()
                if item['name'] is None:
                    item['name'] = data.xpath("@title").extract_first()
                    # yield item
                    # yield self.make_requests_from_url(item['lisnk'])
            except():
                print('===== Something Wrong =====')
        else:
            print('===========================================')
            print('======== Book Session Done Success ========')
            print('===========================================')

    def parse_book_list(self, response):
        datas = response.xpath("//div[@class='v_shop_box ']/div/ul/li")
        redis = Redis(password=self.settings['REDIS_PASSWORD'])
        for data in datas:
            try:
                item = ProductItem()
                item['name'] = data.xpath("a/@title").extract_first()
                item['link'] = data.xpath("a/@href").extract_first()
                item['price'] = \
                    data.xpath("p[@class='price']/span[@class='rob']/span[@class='num']/text()").extract_first() + \
                    data.xpath("p[@class='price']/span[@class='rob']/span[@class='tail']/text()").extract_first()
                yield item
                redis.lpush('dang:book_urls', item['link'])
            except:
                pass


class DangSlaveSpider(RedisSpider):
    name = 'dang_slave'
    redis_key = 'dang:book_urls'
    # book_item_lx = LinkExtractor(allow=(r'http://v.dangdang.com/book',))
    # rules = (
    #     Rule(book_item_lx, callback='parse_book_item')
    # )

    def parse(self, response):

        item = ProductItem()
        print(response.xpath("//*[@id='dd-zhe']").extract_first().encode('utf8'))

        item['link'] = response.url
        item['name'] = response.xpath("//div[@class='sale_box_left']/div[@class='name_info']/h1/text()").extract_first()
        item['price'] = response.xpath("//div[@id='pc-price']/div[@class='price_d']/p[@id='dd-price']/text()").extract_first()
        item['price_origin'] = response.xpath("//div[@id='pc-price']/div[@id='original-price']/text()").extract_first()
        item['price_origin'] = response.xpath("//*[@id='original-price']/text()").extract_first()
        item['discount'] = response.xpath("//*[@id='dd-zhe']/text()").extract_first()
        item['author'] = response.xpath("//div[@class='messbox_info']/span[@id='author']/a/text()").extract_first()
        item['author'] = response.xpath("//div[@class='messbox_info']/span[@id='author']/text()").extract_first()
        item['publish_corp'] = response.xpath("//div[@class='messbox_info']/span[@class='t1'][2]/a/text()").extract_first()
        item['publish_time'] = response.xpath("//div[@class='messbox_info']/span[@class='t1'][3]/text()").extract_first()
        item['book_img'] = response.xpath("//div[@class='pic_info']/div[@id='largePicDiv']/a[@class='img']/img/@src").extract_first()

        for i in item:
            try:
                item[i] = item[i].strip()
            except:
                pass
            else:
                pass

        return item




