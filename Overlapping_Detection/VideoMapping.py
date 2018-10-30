#coding=utf8
import pymysql
import csv
import traceback



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
