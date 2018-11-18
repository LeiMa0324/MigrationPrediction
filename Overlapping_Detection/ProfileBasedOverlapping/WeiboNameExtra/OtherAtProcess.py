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

微博id:
微博【大宅】
微博->亲爱的撒多
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
处理格式
微博：打老虎
微博id：哈哈哈

'''
# 获取新浪xxx冒号后的姓名，不符合要求的colon_name为空
def strip_colon(df,column_name):
    df1 = df
    direct_colon_name = []
    print('获取m冒号后的...')
    for index,row in df1.iterrows():
        try:
            signgroup = re.search(r'.*[微博 围脖 微博ID weibo][：:](.*)', row[column_name], re.M | re.I)
            direct_colon_name.append(signgroup.group(1))
            print(direct_colon_name[index])
        except Exception:
            print("unmatch item, next!")
            direct_colon_name.append(None)
            pass

    df1['colon_name'] = direct_colon_name
    print(df1)
    return df1
'''
处理格式 用空格分割
微博 小美女
'''

def delete_blank(df,column_name):
    df1 = df
    direct_colon_name = []
    print('获取空格后的微博名...')
    for index,row in df1.iterrows():
        try:
            signgroup = re.search(r'.*[微博 微博id][\s+](.*)', row[column_name], re.M | re.I)
            direct_colon_name.append(signgroup.group(1))
            print(direct_colon_name[index])
        except Exception:
            print("unmatch item, next!")
            direct_colon_name.append(None)
            pass

    df1['colon_name'] = direct_colon_name
    print(df1)
    return df1


'''
处理微博名后面的部分
'''

# 去除空格
def strip_blank(df):
    tmp_df = df
    no_blank_name =[]
    print('删除colon中的空格...')
    for index,row in tmp_df.iterrows():
        # colon_num不为空
        if row['colon_name']:
            try:
                signgroup = re.search(r'(.*?)[\s+](.*?)', row['colon_name'], re.M | re.I)
                no_blank_name.append(signgroup.group(1))

            except Exception:
                print("unmatch item, next!")
                no_blank_name.append(row['colon_name'])
                pass
        # colon_num为空
        else:
            no_blank_name.append(None)
            pass

    tmp_df['no_blank'] = no_blank_name
    return tmp_df


# 去除符号
def strip_punc(df):
    tmp_df = df
    no_blank_name =df['no_blank']
    print('删除colon中的符号...')
    punc_str = "(.*?)([，。【】（）丨|“”？；：！（）()!~~.←→╮╭／]+)"
    name_no_punc = []
    for item in no_blank_name:
        # colon_num不为空
        if item:
            try:
                signgroup = re.search(punc_str, item, re.M | re.I)
                name_no_punc.append(signgroup.group(1))

            except Exception:
                print("unmatch item, next!")
                name_no_punc.append(item)
                pass
        # colon_num为空
        else:
            name_no_punc.append(None)
            pass

    tmp_df['name_no_punc'] = name_no_punc
    return tmp_df

'''
插入数据库
'''
def insert_data(df,table_name):
    engine = create_engine('mysql+pymysql://root:123@223.3.76.172/MigrationDetection?charset=utf8')
    df.to_sql(name=table_name,if_exists='replace',con=engine)
    print(df.head())

'''
main 函数
'''
#  处理用冒号分割的微博名
def bili_process():
    # process 1
    sql1 = "SELECT id,signature FROM MigrationDetection.acfun_weibo_other;"
    df1 = get_data(sql1)
    df_no_colon = strip_colon(df1,'signature')
    df_noblank= strip_blank(df_no_colon)
    df_no_blan_no_punc = strip_punc(df_noblank)
    insert_data(df_no_blan_no_punc,'acfun_weibo_other_processed')

# 处理用空格分割的微博名
def blank_split():
    sql1 = "SELECT id,signature FROM MigrationDetection.acfun_weibo_other_nocolon;"
    df1 = get_data(sql1)
    # 获取空格后的微博名+其他信息
    df_name = delete_blank(df1,'signature')
    # 处理微博名后的空格
    df_noblank = strip_blank(df_name)
    # 处理微博名后的标点
    df_no_blan_no_punc = strip_punc(df_noblank)
    insert_data(df_no_blan_no_punc, 'acfun_weibo_other_nocolon_processed')

blank_split()

# bili_process()

# line1 ='新浪微博 方向音痴的企鹅。链接：http://pan.baidu.com/s/1XaFy2 密码：iy34请自取。努力追求KAITO中'
# line2 ='微博id 碳化钙_CaC2'
# line3 ='微博 阿奚_喵了个咪   今天也要好好努力呐（·w·）9'
#
# signgroup = re.search(r'.*[微博 微博id][\s+](.*)', line2, re.M | re.I)
# print(signgroup.group(1))