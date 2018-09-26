import re
import numpy as np
import pandas as pd
import pymysql
import time
from sqlalchemy import create_engine
from string import punctuation

pd.set_option('display.max_columns',1000)
'''
几种签名形式
1、直接写用户名，不包含@
微博：小兔子

2、包含@
微博：@打老虎
微博@莜莜
我的微博是@哈哈哈

3、weibo网址
微博 weibo.com/2094sasd
有可能有http 有可能没有

'''

#链接数据库
conn = pymysql.connect(host="223.3.85.102", user="root", passwd="123", charset="utf8",db='MigrationDetection')

'''
3.提取微博网址
'''
# sign = 'ACG88键音游玩家～\nhttp://weibo.com/u/2432315244'
# 提取weibo.com/后的文字
#sign_processed = re.search(r'(.*)weibo\.com\/(.*?) (.*)$', sign, re.M | re.I)
# sign_processed = re.search(r'(.*)weibo\.com(.*?)$', sign, re.M | re.I)
#
# print(sign_processed.group(2))

'''
获取数据
'''
def get_data(sql):
    df = pd.read_sql(sql=sql,con=conn)
    return df


unmatchcount = 0

'''
3.1 获得去除weibo.com的用户名
'''
def strip_url(df):
    weiboname = []
    for index,row in df.iterrows():
        try:
             signgroup = re.search(r'(.*)weibo\.com\/(.*?)$', row['sign'], re.M | re.I)
             weiboname.append(signgroup.group(2))
             print(weiboname[index])
        except Exception:
            print("unmatch item, next!")
            weiboname.append(None)
            pass

    df.insert(2,'weiboname',weiboname)
    return df



'''
3.2 去除逗号、空格、句号分割的后半部分
'''
def delete_signs(df):
    df1 = df
    # 删除空白
    NewNames = []
    for index,row in df1.iterrows():
        try:
            #去除空格
             signgroup = re.search(r'(\w+)[\s+](.*?)', row['weiboname'], re.M | re.I)
             NewNames.append(signgroup.group(1))
             print(NewNames[index])
        except Exception:
            print("unmatch item, next!")
            NewNames.append(row['weiboname'])
            pass

    # TODO 删除符号，不包括问号
    return NewNames


'''
插入数据库
'''
def insert_data(df):
    engine = create_engine('mysql+pymysql://root:123@223.3.85.102/MigrationDetection?charset=utf8')
    df.to_sql(name='bili_weibo_links',if_exists='append',con=engine)
    print(df.head())

# sign = 'xiaoniaoyoushou   异口同声配音工作室 '
# sign_processed = re.search(r'(\w+)[\s+](.*?)', sign, re.M | re.I)
#
# print(sign_processed.group(1))

sql = "SELECT id,weiboname FROM MigrationDetection.bili_weibo_links;"
df=get_data(sql)


NameWithoutBlank= delete_signs(df)
df.insert(2,'NameWithoutBlank',NameWithoutBlank)
df.to_csv('NameWithoutBlank.csv')
print(df)
