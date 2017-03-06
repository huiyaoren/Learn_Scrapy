# coding: utf8


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:12345678@localhost/beston")
DBSession = sessionmaker(bind=engine)