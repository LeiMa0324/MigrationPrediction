import re
import numpy as np
import pandas as pd
import pymysql
import time
from sqlalchemy import create_engine
from string import punctuation

pd.set_option('display.max_columns',1000)

#链接数据库
conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8",db='MigrationDetection')
'''
2、不包含@
表名：bili_weibo_other
微博：打老虎
weibo:shhah
围脖 asdsa
微博莜莜
我的微博是哈哈哈

'''


'''
获取数据
'''
def get_data(sql):
    df = pd.read_sql(sql=sql,con=conn)
    return df

'''
插入数据库
'''
def insert_data(df,table_name):
    engine = create_engine('mysql+pymysql://root:123@223.3.76.172/MigrationDetection?charset=utf8')
    df.to_sql(name=table_name,if_exists='replace',con=engine)
    print(df.head())


