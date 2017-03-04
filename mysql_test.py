# coding: utf8
from sqlalchemy import create_engine, text, Column, Integer, String, Unicode
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def test_1():
    db = create_engine("mysql+pymysql://root:12345678@localhost/beston")

    # result = db.execute("DROP TABLE IF EXISTS beston.bt_transfer")
    # result = db.execute("CREATE TABLE beston.bt_transfer(transfer_id INT)")
    #
    # result = db.execute(text("ALTER TABLE beston.bt_transfer ADD transfer_order_id INT NULL"))


    # result = db.execute(text("select * from bt_transfer"))

    # result = db.execute(text("select * from bt_transfer where transfer_order_id = :id"), {'id': 345})

    # 指定返回数据的数据类型
    t = text("select * from bt_transfer where transfer_id = :id",
             typemap={'transfer_content': Unicode}
             )
    # t = text("insert into bt_transfer(transfer_order_id, transfer_content) VALUES (:id, 'ccc')",
    #             typemap={'id': Integer}
    #          )
    result = db.execute(t, {'id': '1'})


    # print result.scalar()
    # print result.rowcount
    # print result.fetchmany()
    # print result.fetchall()
    # print result.fetchall()[0].transfer_content
    # print result.fetchone()
    # print result.fetchone()
    # print result.first()

# 创建对象基类
Base = declarative_base()


# 物流表
class Transfer(Base):

    # 表名
    __tablename__ = 'bt_transfer'

    # 表结构
    transfer_id = Column(Integer, primary_key=True)
    transfer_order_id = Column(Integer)
    transfer_content = Column(String(255))
    transfer_order_status = Column()


    # def __int__(self, id, name):
    #     self.id = id
    #     self.name = name


# ORM 操作
def test_2():
    # 初始化连接
    engine = create_engine('mysql+pymysql://root:12345678@localhost:3306/beston')
    # 创建 DBSession 类型
    DBSession = sessionmaker(bind=engine)


    # 创建 session 对象
    session = DBSession()
    # 创建新 User 对象
    new_transfer = Transfer(transfer_content='hello,world')
    # 添加到 session
    session.add(new_transfer)
    # 提交保存
    session.commit()
    # 关闭 session
    session.close()

    session = DBSession()
    # 创建 Query 查询 filter == where, one() 返回唯一行， all() 返回所有行
    transfer = session.query(Transfer).filter(Transfer.transfer_id==1).one()
    # 打印对象类型与对象 transfer_content 属性
    print('type', type(Transfer))
    print('content', transfer.transfer_content)
    session.close()


