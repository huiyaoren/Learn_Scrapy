# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from .model.config import DBSession
from .model.transfer import Transfer


class DangdangPipeline(object):
    def open_spider(self, spider):
        self.session = DBSession()
        self.session.execute('SET NAMES utf8;')
        self.session.execute('SET CHARACTER SET utf8;')
        self.session.execute('SET character_set_connection=utf8;')

    def process_item(self, item, spider):
        if 0:
            raise DropItem("跳过已完成订单")
        else:
            a = Transfer(
                transfer_order_id = item['session_online_id'],
                transfer_content = item['session_name'].encode('utf8')
            )
            self.session.merge(a)
            self.session.commit()
            return item

    def close_spider(self, spider):
        self.session.close()
