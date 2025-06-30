# -*- codeing = utf-8 -*-
# @Desc:
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import pymysql

host = 'bigdata'
user = 'root'
password = '123456'
port = 3306
database = 'Flink_Fliggy_Flight'

DB_URI ='mysql+pymysql://root:'+password+'@'+host+':'+str(port)+'/'+database

engine = create_engine(DB_URI)
#Base = declarative_base()  # SQLORM基类
session = sessionmaker(engine)()  # 构建session对象

cnn = pymysql.connect(host=host, user=user, password=password, port=port, database=database,
                      charset='utf8')