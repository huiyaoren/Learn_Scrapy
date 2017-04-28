# coding: utf8
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:12345678@localhost/beston")
DBSession = sessionmaker(bind=engine)

# 地区查询
engine_1 = create_engine("mysql+pymysql://root:root@122.114.45.160/signin")
AreaSession = sessionmaker(bind=engine_1)
metadata = MetaData(engine_1)
# region_table = Table('si_region', metadata, autoload=True)

session = AreaSession()
session.execute('SET NAMES utf8;')
session.execute('SET CHARACTER SET utf8;')
session.execute('SET character_set_connection=utf8;')

var = {
    "message": "ok",
    "nu": "602205232853",
    "ischeck": "1",
    "condition": "F00",
    "com": "shunfeng",
    "status": "200",
    "state": "3",
    "data": [
        {"time": "2017-03-06 11:00:05", "ftime": "2017-03-06 11:00:05", "context": "已签收,感谢使用顺丰,期待再次为您服务", "location": "null"},
        {"time": "2017-03-04 06:40:22", "ftime": "2017-03-04 06:40:22", "context": "正在派送途中,请您准备签收(派件人:陈武,电话:15980709770)", "location": "null"},
        {"time": "2017-03-04 05:58:49", "ftime": "2017-03-04 05:58:49", "context": "快件到达 【福州晋安华林路营业点】", "location": "【福州晋安华林路营业点】"},
        {"time": "2017-03-04 01:47:48", "ftime": "2017-03-04 01:47:48", "context": "快件在【福州尚干集散中心】已装车，准备发往 【福州晋安华林路营业点】", "location": "【福州晋安华林路营业点】"},
        {"time": "2017-03-04 00:14:42", "ftime": "2017-03-04 00:14:42", "context": "快件到达 【福州尚干集散中心】", "location": "null"},
        {"time": "2017-03-03 19:39:33", "ftime": "2017-03-03 19:39:33", "context": "快件在【三明】已装车，准备发往 【福州尚干集散中心】", "location": "【三明】"},
        {"time": "2017-03-03 19:33:01", "ftime": "2017-03-03 19:33:01", "context": "快件到达 【三明】", "location": "【三明】"},
        {"time": "2017-03-03 18:29:58", "ftime": "2017-03-03 18:29:58", "context": "快件在【三明永安开辉营业点】已装车，准备发往 【三明】", "location": "【三明永安开辉营业点】"},
        {"time": "2017-03-03 15:56:40", "ftime": "2017-03-03 15:56:40", "context": "顺丰速运 已收取快件", "location": "null"}
    ]
}
