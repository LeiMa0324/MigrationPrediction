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
        usermapping =list(set(record))
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

        # csv写入列名
        column_name='a_id,a_username,a_gender,a_sign,b_id,b_name,b_sex,b_sign'

        with open('UsermappingByVideo.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_name)

        for row in usermapping:
            print("写入第%d行"%usermapping.index(row) )
            print("aid:%s bid:%s"%(row[0],row[1]))
            cur = conn.cursor()
            cur.execute(sql,(row[0],row[1]))
            row = cur.fetchone()
            if row:
                usermapping_detail.append(row)
                with open('UsermappingByVideo.csv', 'a', newline='',encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(row)
            else:
                continue

    except Exception:
        print(traceback.print_exc())

# 记录Video数
def CommonVideoCount():
    usermapping=[]
    try:
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8", db='bilibili')
        sql = 'SELECT a_id,b_id FROM bilibili.UsermappingByVideo;'
        cur = conn.cursor()
        cur.execute(sql)
        record = cur.fetchall()
        usermapping = list(record)
        cur.close()
        conn.close()

    except Exception:
        print(traceback.print_exc())

    for row in usermapping:
        tmp_sql ='SELECT count(*) from video_mapping where a_uid =%s and mid =%s;'
        try:
            conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8", db='bilibili')
            cur = conn.cursor()
            cur.execute(tmp_sql,(row[0],row[1]))
            record = cur.fetchone()
            cur.close()
            if record:
                cur1= conn.cursor()
                update_sql = 'update UsermappingByVideo set common_videos=%s where a_id=%s and b_id =%s;'
                cur1.execute(update_sql,(record[0],row[0],row[1]))
                print('完成update：aid：%s,b_id%s,common_video:%d'%(row[0],row[1],record[0]))
                cur1.close()
            conn.commit()
            conn.close()

        except Exception:
            print(traceback.print_exc())

CommonVideoCount()