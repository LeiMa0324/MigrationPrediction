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


acfun_df = pd.read_csv('acfun_weibo_names.csv')
acfun_df['weibo_id'] = np.nan
acfun_df['index'] = acfun_df.index

# acfun 的 dataframe转化为列表
acfun_data = acfun_df.values.tolist()

bili_df = pd.read_csv('bili_weibo_names.csv')
bili_df['weibo_id'] = np.nan
bili_df['index'] = bili_df.index
# bili 的 dataframe转化为列表
bili_data = bili_df.values.tolist()





# 写入 acfun 文件
def acfun_to_csv(row):
    # 将 acfun 数据写入 csv 文件
    with open('acfun_weibo_name_with_id_001.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

# 写入 bili 文件
def bili_to_csv(row):
    # 将 acfun 数据写入 csv 文件
    with open('bili_weibo_name_with_id_001.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

# 获取单个acfun用户的 id
def get_acfun_id(data):
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8", db='weibo001')
    table_name ="weibouser"+table_index
    containerid_sql = 'select containerid from %s '%table_name
    containerid_sql += 'where nickname =%s;'

    print("在数据库 weibo001的 weibouser%s表查找acfun第%i 个用户..." % (table_index,data[4]))
    try:
        cur = conn.cursor()
        cur.execute(containerid_sql,data[2])
        record = cur.fetchone()
        # 如果查找到用户
        if record:
            print("查找到同名用户")
            # 将 weibo_id 设置为 containerid
            data[3] = record[0]
            # 将该数据写入文件中
            acfun_to_csv(data)
            print(record[0])
            # 将该数据从 acfun_data 中删除
            try:
                acfun_data.remove(data)
            except Exception:
                print(Exception)

            print("完成插入数组")
        else:
            print("未查到找同名用户，查找下一个用户")
            pass
    except Exception as err:
        print("发生错误，用户号%s"%data[2])
        print(err)
        print(traceback.print_exc())
        time.sleep(20)
    conn.close()

# 获取单个bili用户的 id
def get_bili_id(data):
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8", db='weibo001')
    table_name ="weibouser"+table_index
    containerid_sql = 'select containerid from %s '%table_name
    containerid_sql += 'where nickname =%s;'

    print("在数据库 weibo001的 weibouser%s表查找bili第%d 个用户..."% (table_index,data[4]))
    try:
        cur = conn.cursor()
        cur.execute(containerid_sql,data[2])
        record = cur.fetchone()
        # 如果查找到用户
        if record:
            print("查找到同名用户")
            # 将 weibo_id 设置为 containerid
            data[3] = record[0]
            # 将该数据写入文件中
            bili_to_csv(data)
            print(record[0])
            # 将该数据从 acfun_data 中删除
            try:
                bili_data.remove(data)
            except Exception:
                print(Exception)

            print("完成插入数组")
        else:
            print("未查到找同名用户，查找下一个用户")
            pass
    except Exception:
        print("发生错误，用户号%s"%data[2])
        print(Exception)
    conn.close()


# 开启多线程
def mul(func_name,datas):
    # 开启4个线程
    pool = ThreadPool(4)
    try:
        results = pool.map(func_name, datas)

    except Exception:
        # print 'ConnectionError'
        print(Exception)
        # 用map函数代替for循环，开启多线程运行函数
        results = pool.map(func_name, datas)

    pool.close()
    pool.join()



#在database001中20个表中遍历
'''
在 weibo001中查找 name 的 id
'''
#  遍历20个表名
for i in range(0,20):
    if int(i/10)==0:
        table_index ='0'+str(i)
    else:
        table_index = str(i)
    print("查询第%s 个数据库"%table_index)

    '''
    多线程处理 acfun 数据
    '''
    mul(get_acfun_id,acfun_data)
    '''
    多线程处理 bili 数据
    '''
    mul(get_bili_id, bili_data)

print("weibo001中20个表查询完毕！")



