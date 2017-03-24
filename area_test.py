# coding: utf8
# from __future__ import unicode_literals
from urllib import urlencode

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



engine_1 = create_engine("mysql+pymysql://root:root@122.114.45.160/signin?charset=utf8")
AreaSession = sessionmaker(bind=engine_1)
metadata = MetaData(engine_1)
region_table = Table('si_region', metadata, autoload=True)



# for i in result.fetchall():
#     print(i[2])
#     print()

# str = u'福州'
# str = str.encode('gb2312')
# d = {'area': str}
# print(urlencode(d))

# results = session.execute('select region_id, region_name from si_region where TRUE ')

# for r in results.fetchall():
#
#     area = r.region_name.decode('utf8').encode('gbk')
#     d = {
#         'action': 'area2zone',
#         'area': area
#     }
#     url = 'http://www.ip138.com/post/search.asp?' + urlencode(d)
#     print(url)


Base = declarative_base()
# 物流表
class Region(Base):

    # 表名
    __tablename__ = 'si_region'

    __table_args__ = {
        'mysql_engine': 'MyISAM',
        'mysql_charset': 'utf8'
    }

    # 表结构
    region_id = Column(Integer, primary_key=True)
    region_name = Column(String(100))
    region_area_number = Column(String(8))

if __name__ == '__main__':
    engine_1 = create_engine("mysql+pymysql://root:12345678@localhost/test")
    AreaSession = sessionmaker(bind=engine_1)
    session = AreaSession()

    query1 = session.query(Region)
    print query1.filter(Region.region_id == 1).update({'region_id': 2})
    session.commit()


    # session.execute("SET NAMES utf8")
    # session.execute("SET CHARACTER SET utf8")
    # session.execute("SET character_set_connection = 'utf8'")
    # session.execute("set character_set_results = 'utf8'")
    # session.execute("set character_set_client = 'utf8'")
    # result = session.execute(text(u"update si_region set region_name='福州市1' where region_name='福州市'"))
    # result = session.execute(u"select * from si_region where region_name='福州市'")
    # region_id = result.fetchall()[0].region_id
    # session.execute(text("update si_region set region_id=2 where region_id=1;"))
    # result = session.execute(text("select * from si_region where 1"))



