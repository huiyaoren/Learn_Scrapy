# coding:utf8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 物流表
class Transfer(Base):

    # 表名
    __tablename__ = 'bt_transfer'

    __table_args__ = {
        'mysql_engine': 'MyISAM',
        'mysql_charset': 'utf8'
    }

    # 表结构
    transfer_id = Column(Integer, primary_key=True)
    transfer_order_id = Column(Integer)
    transfer_content = Column(String(255))
    transfer_order_status = Column()
