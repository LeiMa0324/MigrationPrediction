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
获取数据
'''
def get_data(sql):
    df = pd.read_sql(sql=sql,con=conn)
    return df



'''
3、weibo网址 ✔
表明：bili_weibo_links
微博 weibo.com/2094sasd
有可能有http 有可能没有
'''


'''
3.1 获得去除weibo.com的用户名
'''
def strip_url(df,column_name):
    weiboname = []
    for index,row in df.iterrows():
        try:
             signgroup = re.search(r'(.*)weibo\.com\/(.*?)$', row[column_name], re.M | re.I)
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
def delete_signs(df,column_name):
    df1 = df
    # 删除空白
    processed_name = []
    print('删除空白...')
    for index,row in df1.iterrows():
        try:
            #去除空格
             signgroup = re.search(r'(\w+)[\s+](.*?)', row[column_name], re.M | re.I)
             processed_name.append(signgroup.group(1))
             print(processed_name[index])
        except Exception:
            print("unmatch item, next!")
            processed_name.append(row[column_name])
            pass
    df1['name_no_blank'] = processed_name


    #删除中文u'[\u4e00-\u9fff]+'
    print('删除中文...')
    name_no_chinese=[]
    chi_str = "(.*?)([\u4E00-\u9FA5]+)"
    for item in processed_name:
        print(item)
        if item is None:
            print("None item")
            name_no_chinese.append(None)
            pass
        else:
            new_item = re.search(chi_str, item, re.M | re.I)
            if new_item:
                name_no_chinese.append(new_item.group(1))
            else:
                print("unmatch item, next!")
                name_no_chinese.append(item)

    df1['no_chinese'] = name_no_chinese


    #删除，。【】)( |
    print("删除标点...")
    name_no_punc = []
    punc_str = "(.*?)([，。【】（）|“”？；：！（）()!~~_.←→╮╭]+)"
    for item in name_no_chinese:
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


'''
插入数据库
'''
def insert_data(df,table_name):
    engine = create_engine('mysql+pymysql://root:123@223.3.76.172/MigrationDetection?charset=utf8')
    df.to_sql(name=table_name,if_exists='replace',con=engine)
    print(df.head())


'''
main
'''



def process_weibo_links():

    sql = "SELECT id,signature FROM MigrationDetection.acfun_weibo_links;"
    df= get_data(sql)
    df1 = strip_url(df,'signature')
    df2= delete_signs(df1,"weiboname")
    insert_data(df2, 'acfun_weibo_links_no_blank')




'''
正则test
'''
# line ='这里轨夙 请不大意的和我说话w微博@K等着杰奇回来 这个号专职搬运啦~搬运君话唠无误w发的视频比较杂乱什么都有 总之就是类似杂物堆积处的感觉'
# signgroup = re.search(r'(.*?)(@.*)', line, re.M | re.I)
# print(signgroup.group(2))
