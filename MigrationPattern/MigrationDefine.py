import pymysql
import numpy as np
import Levenshtein
import difflib
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties  # 步骤一
import re
import csv

# 获取用户在A站和B站上最后一次更新时间
def lastUpdateOnAcfun():
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    acIDS = ()
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        # A站
        # sql = "SELECT a_id from overlap_user_final; "
        # B站
        sql = "SELECT b_id from overlap_user_final; "
        cur.execute(sql)
        acIDS = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()


    acIDList = []
    # 转化为list
    for row in acIDS:
        new_row = list(row)
        acIDList.append(new_row)

    print(acIDList)

    #获取在A站上最新更新时间
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    lastupdateTime =[]
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        # A站
        # sql = "SELECT uid,contributeTime FROM MigrationDetection01.overlap_acfun_videos where uid =%s order by contributeTime desc limit 1; "
        # B站
        sql = "SELECT mid,created FROM MigrationDetection01.overlap_bili_videos where mid =%s order by created desc limit 1; "
        for ac in acIDList:
            cur.execute(sql,ac)
            record = cur.fetchone()
            lastupdateTime.append(list(record))
    except Exception:
        print(Exception)
    finally:
        conn.close()

    print(lastupdateTime)
    # 更新到数据库
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    # try:
    conn.select_db("MigrationDetection01")
    cur = conn.cursor()
    # B站
    sql = "update overlap_user_final set b_lastupdate =%s where b_id = %s;"
    for ac in lastupdateTime:
        cur.execute(sql,(ac[1],ac[0]))
    conn.commit()
# except Exception:
#     print(Exception)
# finally:
    conn.close()

lastUpdateOnAcfun()