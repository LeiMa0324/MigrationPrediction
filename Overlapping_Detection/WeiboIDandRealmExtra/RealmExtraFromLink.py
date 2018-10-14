import re
import numpy as np
import pandas as pd
import pymysql
import time
from sqlalchemy import create_engine
from string import punctuation

'''
realm/profile
realm/home
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


def delete_id_suffix():
    #
    sql = 'SELECT * FROM bili_weibo_links_processed where no_punc regexp "^[0-9a-z]*/.*" and weibo_id is null;'
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
        print(data[6])
        # 处理 no_punc 字段
        signgroup = re.search(r'^([0-9a-z]*)(/.*)', data[6], re.M | re.I)
        result['no_punc'] =signgroup.group(1)
        result['weibo_id'] = data[7]
        result['weibo_realm_name'] =  signgroup.group(1)
        print(result['weibo_realm_name'])
        dictData.append(result)

    update_sql = 'update bili_weibo_links_processed set no_punc =%s,weibo_realm_name=%s where id = %s;'
    for dict in dictData:
        try:
            cur = conn.cursor()
            conn.select_db('MigrationDetection')
            cur.execute(update_sql,(dict['no_punc'],dict['weibo_realm_name'],dict['id']))
            conn.commit()
        except Exception:
            print(Exception)

delete_id_suffix()

# line = 'amfairydanceix/home?wvr=5&amp;c=pr_qdhz_bd_360jllqcj_weibo'
# line2 ='qingyouyouyou/home?wvr=5&amp;lf'
# signgroup = re.search(r'^([0-9a-z]*)(/.*)', line, re.M | re.I)
# print(signgroup.group(1))
