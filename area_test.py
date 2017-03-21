# coding: utf8
from urllib import urlencode

from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine_1 = create_engine("mysql+pymysql://root:root@122.114.45.160/signin")
AreaSession = sessionmaker(bind=engine_1)
metadata = MetaData(engine_1)
region_table = Table('si_region', metadata, autoload=True)

session = AreaSession()
session.execute('SET NAMES utf8;')
session.execute('SET CHARACTER SET utf8;')
session.execute('SET character_set_connection=utf8;')
# result = session.execute('select * from si_region where TRUE ')

# for i in result.fetchall():
#     print(i[2])
#     print()

# str = u'福州'
# str = str.encode('gb2312')
# d = {'area': str}
# print(urlencode(d))

results = session.execute('select region_id, region_name from si_region where TRUE ')

for r in results.fetchall():

    area = r.region_name.decode('utf8').encode('gbk')
    d = {
        'action': 'area2zone',
        'area': area
    }
    url = 'http://www.ip138.com/post/search.asp?' + urlencode(d)
    print(url)