# coding: utf8

from scrapy import FormRequest
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine, text, Column, Integer, String, Unicode, or_, not_, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from random import randint


def test_1():
    db = create_engine("mysql+pymysql://root:12345678@localhost/beston")

    # result = db.execute("DROP TABLE IF EXISTS beston.bt_transfer")
    # result = db.execute("CREATE TABLE beston.bt_transfer(transfer_id INT)")
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

# 创建表
def init_db():
    Base.metadata.create_all(engine)

# 删除表
def drop_db():
    Base.metadata.drop_all(engine)


# 物流表
class Transfer(Base):

    # 表名
    __tablename__ = 'bt_transfer'

    __table_args__ = {
        'mysql_engine': 'MyISAM',
        'mysql_charset': 'utf8'
    }

    # 表结构
    transfer_id = Column(Integer, primary_key=True, autoincrement=True)
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

    # ====================================
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
    # ====================================


    # ====================================
    session = DBSession()
    # 创建 Query 查询 filter == where, one() 返回唯一行， all() 返回所有行，
    transfer = session.query(Transfer).filter(Transfer.transfer_id==1).one()
    # 打印对象类型与对象 transfer_content 属性
    print('type', type(Transfer))
    print('content', transfer.transfer_content)
    session.close()
    # ====================================

def test_3():

    engine = create_engine("mysql+pymysql://root:12345678@localhost/beston")
    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    result = session.execute('select * from bt_transfer')

    print(result.fetchall())

# ORM
def test_4():
    engine = create_engine("mysql+pymysql://root:12345678@localhost:3306/beston")
    DBSession = sessionmaker(engine)

    session = DBSession()
    query1 = session.query(Transfer)

    # 打印 SQL 语句
    print query1
    print query1.statement

    # 遍历时查询
    for transfer in query1:
        print transfer

    # 以主键获取
    print query1.get(1).transfer_content

    # filter 支持字符串
    print query1.filter('transfer_id = 1')

    # limit
    print query1.limit(1).all()
    print query1.offset(2).all()

    # order
    print query1.order_by(Transfer.transfer_id).all()
    print query1.order_by('transfer_id').all()
    print query1.order_by(Transfer.transfer_id.desc()).all()
    print query1.order_by(text('transfer_content desc')).all() # 官方推荐使用 text() 对 SQL 语句预处理
    print query1.order_by(Transfer.transfer_id.desc(), Transfer.transfer_content).all()

    # scalar 如果有记录 返回第一条记录的第一个元素 结果不唯一时返回错误
    print query1.filter(Transfer.transfer_id == 1).scalar()
    print session.query('transfer_id').select_from(Transfer).filter('transfer_id = 1').scalar()

    # and 拼接 filter
    print query1.filter(Transfer.transfer_id > 1, Transfer.transfer_content != '').all()
    print query1.filter(Transfer.transfer_id > 1).filter(Transfer.transfer_content != '').all()

    # or 拼接
    print query1.filter(or_(Transfer.transfer_id == 1, Transfer.transfer_id == 2)).scalar()

    # in 筛选
    print query1.filter(Transfer.transfer_id.in_((1, 2))).all()

    # null
    print query1.filter(Transfer.transfer_order_id == None).all()
    print query1.filter(text('transfer_order_id is null')).all()
    print query1.filter(not_(Transfer.transfer_order_id == None)).all()
    print query1.filter(Transfer.transfer_id != None).all()

    # func.count
    print session.query(func.count('*')).select_from(Transfer).all()
    print session.query(func.count('1')).select_from(Transfer).all()
    print session.query(func.count(Transfer.transfer_id)).scalar()
    print session.query(func.count(Transfer.transfer_id)).filter(Transfer.transfer_id > 0).scalar() # filter 中包含 Transfer 因此不需要指定表
    print session.query(func.count(Transfer.transfer_id)).filter(Transfer.transfer_id > 0).limit(1).scalar()

    # func....
    print session.query(func.sum(Transfer.transfer_id)).all()
    print session.query(func.now()).all()
    print session.query(func.current_timestamp()).all()
    print session.query(func.md5('asdf')).all()

    # update
    print query1.filter(Transfer.transfer_id == 9).update({'transfer_order_id': 666})

    transfer = query1.get(11)
    transfer.transfer_order_id = 22
    session.flush() # 提交修改

    # delete
    session.delete(transfer) # 暂不执行
    session.rollback() # 回退
    session.commit() # 提交

    query1.filter(Transfer.transfer_id == 11).delete() # 直接删除


# 插入大量随机数据
def add_lot_data():
    engine = create_engine("mysql+pymysql://root:12345678@localhost/beston")
    DBSession = sessionmaker(bind=engine)
    session = DBSession()


    session.execute(
        Transfer.__table__.insert(),
        [{'transfer_order_id': randint(1,100)} for i in range(10)]
    )

# 替换一个已知主键的记录
def replace_id_data():
    engine = create_engine("mysql+pymysql://root:12345678@localhost/beston")
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    transfer = Transfer(transfer_id = 12, transfer_content='qwer')
    session.merge(transfer)
    session.commit()

# 当字段为关键字时的处理方法
from_ = Column('from', String(10))

# 无法删除 in 操作查询出来的记录？
def delete_in():
    engine = create_engine("mysql+pymysql://root:12345678@localhost/beston")
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.query(Transfer).filter(Transfer.transfer_id.in_((1,2,3))).delete(synchronize_session=False)
    session.commit()




class ModelMixin(object):
    @classmethod
    def get_by_id(cls, session, id, columns=None, lock_mode=None):
        if hasattr(cls, 'id'):
            scalar = False
            if columns:
                if isinstance(columns, (tuple, list)):
                    query = session.query(*columns)
                else:
                    scalar = True
                    query = session.query(columns)
            else:
                query = session.query(cls)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            query = query.filter(cls.id == id)
            if scalar:
                return query.scalar()
            return query.first()
        return None
    Base.get_by_id = get_by_id
    @classmethod
    def get_all(cls, session, columns=None, offset=None, limit=None, order_by=None, lock_mode=None):
        if columns:
            if isinstance(columns, (tuple, list)):
                query = session.query(*columns)
            else:
                query = session.query(columns)
                if isinstance(columns, str):
                    query = query.select_from(cls)
        else:
            query = session.query(cls)
        if order_by is not None:
            if isinstance(order_by, (tuple, list)):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.all()
    Base.get_all = get_all
    @classmethod
    def count_all(cls, session, lock_mode=None):
        query = session.query(func.count('*')).select_from(cls)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.scalar()
    Base.count_all = count_all
    @classmethod
    def exist(cls, session, id, lock_mode=None):
        if hasattr(cls, 'id'):
            query = session.query(func.count('*')).select_from(cls).filter(cls.id == id)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            return query.scalar() > 0
        return False
    Base.exist = exist
    @classmethod
    def set_attr(cls, session, id, attr, value):
        if hasattr(cls, 'id'):
            session.query(cls).filter(cls.id == id).update({
                attr: value
            })
            session.commit()
    Base.set_attr = set_attr
    @classmethod
    def set_attrs(cls, session, id, attrs):
        if hasattr(cls, 'id'):
            session.query(cls).filter(cls.id == id).update(attrs)
            session.commit()
    Base.set_attrs = set_attrs

class Base(Base):
    __abstract__ = True
    __table_args__ = {  # 可以省掉子类的 __table_args__ 了
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

def test(response):
    print response



