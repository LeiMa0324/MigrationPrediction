import re
import numpy as np
import pandas as pd
import pymysql
import time
from sqlalchemy import create_engine
from string import punctuation


'''
从bili_weibo_links_processed 和acfun_weibo_links_processed
中提取每个用户的 id 或者个性域名
用于匹配重叠用户

link 类型
1. 带id 的 profile 的类型
'1168437882/profile?topnav=1&amp;wvr=6'
2. 带 u 的 id 的类型
'u/5508869514'
3. 带 p 的 id 的类型
'p/1005052284381983'
4. 单独的 id
'548012091'
5. 单独的个性域名，以字母或数字开头
'ArryZ'
'''

conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8",db='MigrationDetection')



def get_data(sql):
    df = pd.read_sql(sql=sql,con=conn)
    return df


def update_data(dictData,update_sql):
    for dict in dictData:
        try:
            cur = conn.cursor()
            conn.select_db('MigrationDetection')
            cur.execute(update_sql,(dict['weibo_id'],dict['id']))
            conn.commit()
        except Exception:
            print(Exception)

'''
选择形为：id/profilexxx.com 或者 id/home.com 的类型
12390234230/profil?
4324923409/home?
'''
def delete_id_suffix():
    #
    sql = 'SELECT * FROM bili_weibo_links_processed where no_punc regexp "^[0-9]*/.*";'
    df = get_data(sql)
    # 将 df 文件转化为数组
    dataarray = df.values
    dictData =[]

    for data in dataarray:
        result ={}
        result['index'] =data[0]
        result['id'] = data[1]
        result['sign'] = data[2]
        result['weiboname'] = data[3]
        result['name_no_blank'] = data[4]
        result['no_chinese'] = data[5]
        result['no_punc'] = data[6]
        print(result['no_punc'])
        # 处理 no_punc 字段
        signgroup = re.search(r'^([0-9]*)(/.*)', data[6], re.M | re.I)
        result['weibo_id'] = signgroup.group(1)
        print(result['weibo_id'])
        result['weibo_realm_name'] = data[8]
        dictData.append(result)

    update_sql = 'update bili_weibo_links_processed set weibo_id=%s where id = %s;'
    update_data(dictData,update_sql)

'''
p/23432423523/
u/3243242344/xxx
'''
def delete_id_prefix():

    sql = 'SELECT * FROM bili_weibo_links_processed where no_punc regexp "^[u|p][/|?][0-9]*/.*" and weibo_id is null;'
    df = get_data(sql)
    # 将 df 文件转化为数组
    dataarray = df.values
    dictData =[]

    for data in dataarray:
        result ={}
        result['index'] =data[0]
        result['id'] = data[1]
        result['sign'] = data[2]
        result['weiboname'] = data[3]
        result['name_no_blank'] = data[4]
        result['no_chinese'] = data[5]
        result['no_punc'] = data[6]
        print(result['no_punc'])
        # 处理 no_punc 字段
        signgroup = re.search(r'^[u|p][/|?]([0-9]*)/.*', data[6], re.M | re.I)
        result['weibo_id'] = signgroup.group(1)
        print(result['weibo_id'])
        result['weibo_realm_name'] = data[8]
        dictData.append(result)

    update_sql = 'update bili_weibo_links_processed set weibo_id=%s where id = %s;'
    update_data(dictData,update_sql)


delete_id_prefix()


# line = 'u/5289852949/profile?rightmod=1&amp;wvr=6&amp;mod=peroninfo'
# line2 ='p/1005055247482951/home'
# signgroup = re.search(r'^[u|p]/([0-9]*)/.*', line2, re.M | re.I)
# print(signgroup.group(1))