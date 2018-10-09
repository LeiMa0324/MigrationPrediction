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
2、包含@
表名：bili_weibo_at
微博：@打老虎
微博@莜莜
我的微博是@哈哈哈

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


def strip_aate(df,column_name):
    df1 = df
    aate_name = []
    print('获取艾特微博名...')
    for index,row in df1.iterrows():
        try:
             signgroup = re.search(r'(.*?)(@.*)', row[column_name], re.M | re.I)
             aate_name.append(signgroup.group(2))
             print(aate_name[index])
        except Exception:
            print("unmatch item, next!")
            aate_name.append(row[column_name])
            pass
    df1['aate_name'] = aate_name
    print(df1)
    return df1

# 删除空白
def delete_blank(df,column_name):
    df1 = df
    # 删除空白
    processed_name = []
    print('删除空白...')
    for index,row in df1.iterrows():
        try:
            #去除空格
             signgroup = re.search(r'(@.*?)[\s+](.*?)', row[column_name], re.M | re.I)
             processed_name.append(signgroup.group(1))
             print(processed_name[index])
        except Exception:
            print("unmatch item, next!")
            processed_name.append(row[column_name])
            pass
    df1['name_no_blank'] = processed_name
    return df1

# 删除标点
def delete_punc(df):
    #删除，。【】)( |
    df1 = df
    print("删除标点...")
    name_no_blank=df['name_no_blank']
    name_no_punc = []
    punc_str = "(.*?)([，。【】（）|“”？；：！（）()!~~.←→╮╭丶]+)"
    for item in name_no_blank:
        if item is None:
            print("None item")
            name_no_punc.append(None)
            pass
        else:
            new_item = re.search(punc_str, item, re.M | re.I)
            if new_item:
                name_no_punc.append(new_item.group(1))
            else:
                print("unmatch item, next!")
                name_no_punc.append(item)

    df1['no_punc']=name_no_punc
    return df1


def bili_process():
    sql= "SELECT mid,sign FROM MigrationDetection.bili_weibo_at;"
    df = get_data(sql)
    df1= strip_aate(df,'sign')
    df2 = delete_blank(df1,'aate_name')
    df_final= delete_punc(df1)
    insert_data(df_final, 'bili_weibo_at_processed')

def acfun_process():
    sql= "SELECT id,signature FROM MigrationDetection.acfun_weibo_at;"
    df = get_data(sql)
    df1= strip_aate(df,'signature')
    df2 = delete_blank(df1,'aate_name')
    df_final= delete_punc(df1)
    insert_data(df_final, 'acfun_weibo_at_processed')


acfun_process()

'''
正则test
'''
# line ='这里轨夙 请不大意的和我说话w微博@K等着杰奇回来 这个号专职搬运啦~搬运君话唠无误w发的视频比较杂乱什么都有 总之就是类似杂物堆积处的感觉'
# signgroup = re.search(r'(.*?)(@.*)', line, re.M | re.I)
# print(signgroup.group(2))