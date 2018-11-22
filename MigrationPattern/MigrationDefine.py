import pymysql
import numpy as np
import Levenshtein
import difflib
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties  # 步骤一
import re
import csv
import  datetime
import traceback


def getTimeStamp(date):

    return datetime.datetime.strptime(date,'%Y-%m-%d %H:%M').timestamp()

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

# 将用户的视频按照时间顺序排列
def UpdateVector():
    # 提取所有重叠用户对
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    # 重叠用户对
    userPairs =[]
    print('查找重叠用户对...')
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        userpairsql = 'SELECT a_id,b_id FROM MigrationDetection01.overlap_user_final;'
        cur.execute(userpairsql)
        records = cur.fetchall()
        for r in records:
            userPairs.append(list(r))

    except Exception:
        print(Exception)
    finally:
        conn.close()
    print(userPairs)

    # 找对一个重叠用户的所有视频
    allVideoList =[]
    for pair in userPairs:
        userVideos =[]
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection01")
            cur = conn.cursor()
            videosql = 'SELECT a_id,b_id,vid,title,created,abFlag FROM MigrationDetection01.overlap_all_videos where a_id =%s and b_id =%s;'
            cur.execute(videosql,(pair[0],pair[1]))
            videorecords = cur.fetchall()
            for r in videorecords:
                userVideos.append(list(r))
            # 对视频按照上传时间排序
            sorteduserVideos = sorted(userVideos,key=lambda video:getTimeStamp(video[4]))
            allVideoList.extend(sorteduserVideos)

        except Exception as err:
            print(err)
            print(traceback.print_exc())
        finally:
            conn.close()

    print(allVideoList[0])
    print('inserting...')

    # 插入数据库
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        insertsql = 'INSERT INTO sortedVideo(a_id,b_id,vid,title,created,abFlag) values(%s,%s,%s,%s,%s,%s);'
        cur.executemany(insertsql, allVideoList)
        conn.commit()

    except Exception as err:
        print(err)
        print(traceback.print_exc())
    finally:
        conn.close()

UpdateVector()

