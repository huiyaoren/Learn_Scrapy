# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()


class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()

class Profile(Item):

    header_url = Field()
    pic_urls = Field()
    username = Field()
    monologue = Field()
    age = Field()
    source = Field()
    source_url = Field()
    crawled = Field()
    spider = Field()


class CategoryItem(Item):
    name = Field()
    link = Field()

class ProductItem(Item):
    name = Field()
    link = Field()
    price = Field()
    price_origin = Field()
    discount = Field()
    author = Field()
    publish_time = Field()
    publish_corp = Field()
    book_img = Field()



