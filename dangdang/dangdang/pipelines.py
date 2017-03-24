# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from .model.config import DBSession
from .model.config import session
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


class AreaPipeline(object):
    def open_spider(self, spider):
        # engine_1 = create_engine("mysql+pymysql://root:12345678@localhost/test?charset=utf8")
        engine_1 = create_engine("mysql+pymysql://root:root@122.114.45.160/signin?charset=utf8")
        AreaSession = sessionmaker(bind=engine_1)
        self.session = AreaSession()
        self.session.execute('SET NAMES utf8;')
        self.session.execute('SET CHARACTER SET utf8;')
        self.session.execute('SET character_set_connection=utf8;')


    def process_item(self, item, spider):
        # engine_1 = create_engine("mysql+pymysql://root:root@122.114.45.160/signin")

        try:
            self.session.execute(
                text("update si_region set region_area_number=:region_area_number where region_name=:region_name"),
                {
                    'region_area_number': item['region_area_number'],
                    'region_name': item['region_name'].encode('utf8')
                }
            )
            self.session.commit()
        except:
            pass
        return item

    def close_spider(self, spider):
        self.session.close()
