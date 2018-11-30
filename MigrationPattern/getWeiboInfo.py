import re
import numpy as np
import pandas as pd
import pymysql
import csv
from multiprocessing.dummy import Pool as ThreadPool
import time
import traceback
from sqlalchemy import create_engine
from string import punctuation

def getWeiboIDs():
    IDs =[]
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8", db='MigrationDetection02')
    try:
        cur = conn.cursor()
        sql = 'SELECT weibo_id FROM MigrationDetection02.overlap_user_final where weibo_id is not null;'
        cur.execute(sql)
        records = cur.fetchall()
        for r in records:
            IDs.append(r[0])
    except Exception:
        print(Exception)
    finally:
        conn.close()
    print(IDs)
    return IDs


# 获取单个acfun用户的 id
def getWeiboInfo(weiboid):
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8", db='weibo001')
    table_name ="weibouser"+table_index
    containerid_sql = 'select * from %s '%table_name
    containerid_sql += 'where containerid =%s;'

    print("在数据库 weibo001的 weibouser%s表查找用户.%s.." % (table_index,weiboid))
    try:
        cur = conn.cursor()
        cur.execute(containerid_sql,weiboid)
        record = cur.fetchone()
        # 如果查找到用户
        if record:
            print("查找到同名用户")
            # 插入MigrationDetection02中
            SaveUserInfo(list(record)[1:])
            IDs.remove(weiboid)

        else:
            print("未查到找同名用户，查找下一个用户")
            pass
    except Exception as err:
        print("发生错误，用户号%s"%weiboid)
        print(err)
        print(traceback.print_exc())
        time.sleep(20)
    conn.close()

def SaveUserInfo(userInfo):
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8", db='MigrationDetection02')
    try:
        cur = conn.cursor()
        sql = 'INSERT INTO weibouser(containerid,nickname,tag,sex,location,introduction,authentication,sinalevel,school,regtime,imageurl,followerscount,followcount,status,layer)' \
              'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        cur.execute(sql,userInfo)
        conn.commit()
    except Exception:
        print(Exception)
    finally:
        conn.close()
    print('保存成功！')


#在database001中20个表中遍历
'''
在 weibo001中查找 name 的 id
'''

table_index=''
IDs = getWeiboIDs()

#  遍历20个表名
for i in range(0,20):
    if int(i/10)==0:
        table_index ='0'+str(i)
    else:
        table_index = str(i)
    print("查询第%s 个数据库"%table_index)
    for id in IDs:
        getWeiboInfo(id)








