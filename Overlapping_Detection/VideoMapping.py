#coding=utf8
import pymysql
import csv
import traceback
import numpy as np
import pandas as pd
from sqlalchemy import create_engine



# 匹配a站和b站的视频名称
def videomapping():
    for i in range(4,9):
        ac_table_suffix = '0'+str(i)
        ac_table_name = 'acfun_video'+ac_table_suffix

        for j in range(1,10):

            bili_table_suffix = '0'+ str(j)
            bili_table_name = 'bili_video'+bili_table_suffix
            print('查询表：', ac_table_name,bili_table_name)
            new_table_name = 'mapping_video0'+ str(i)+str(j)
            print(new_table_name)
            sql ='create table %s select a.index as a_index,a.vid as a_vid,a.uid as a_uid,a.title as a_title,b.*'%new_table_name
            sql += ' from %s as a,'%ac_table_name
            sql += '%s as b where a.title = b.title;'%bili_table_name
            try:
                conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8", db='bilibili')
                cur = conn.cursor()
                cur.execute(sql)
                cur.close()
                conn.close()
            except Exception as err:
                print('数据库错误')
                print(err)
                print(traceback.print_exc())

# 获取视频up主的id并获取配对数
def usermapping():

    usermapping=()
    try:
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8", db='bilibili')
        sql = 'SELECT a_uid,mid FROM bilibili.video_mapping;'
        cur = conn.cursor()
        cur.execute(sql)
        record = cur.fetchall()
        #获取唯一的(aid,bid)
        usermapping = set(record)
        cur.close()
        conn.close()
        print(len(usermapping))


    except Exception:
        print(Exception)

    usermapping_detail =[]
    try:
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8", db='bilibili')
        sql = 'SELECT a.id as a_id,a.username as a_username,a.gender as a_gender,a.signature as a_sign,' \
              'b.mid as b_id,b.name as b_name,b.sex as b_sex,b.sign as b_sign'\
              ' FROM bilibili.acfun_uppers_detail as a, bilibili_uppers_detail as b' \
              ' where a.id=%s and b.mid=%s;'
        for row in usermapping:
            cur = conn.cursor()
            print(sql)
            cur.execute(sql,(row[0],row[1]))
            row = cur.fetchone()
            usermapping_detail.append(row)
            with open('UsermappingByVideo.csv', 'a', newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)

    except Exception:
        print(traceback.print_exc())

    print(len(usermapping_detail))

    usermapping_detail_DF = pd.read_csv('UsermappingByVideo.csv')
    usermapping_detail_DF.columns=['a_id','a_username','a_gender','a_sig','b_id','b_name','b_sex','b_sign']
    engine = create_engine('mysql+pymysql://root:123@223.3.76.172/MigrationDetection?charset=utf8')
    usermapping_detail_DF.to_sql(name='UsermappingByVideo',if_exists='replace',con=engine)

usermapping()