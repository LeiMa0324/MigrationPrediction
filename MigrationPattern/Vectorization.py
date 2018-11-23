import pymysql
import traceback


'''
对用户上传视频的行为进行向量化
'''
# 获取重叠用户数据
def getUserPairs():
    Userpairs=[]
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    try:
        conn.select_db("MigrationDetection02")
        cur = conn.cursor()
        sql ="SELECT a_id,b_id FROM MigrationDetection02.overlap_behav_vector group by a_id,b_id;"
        cur.execute(sql)
        records = cur.fetchall()
        for r in records:
            Userpairs.append(list(r))
    except Exception:
        print(Exception)
    finally:
        conn.close()
    return Userpairs


# 获取一对重叠用户视频数据
def getVideosForUser(userPair):
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    VideoListForUser =[]
    try:
        conn.select_db("MigrationDetection02")
        cur = conn.cursor()
        sql = "SELECT vid,abFlag,closeupdateFlag FROM MigrationDetection02.overlap_behav_vector where a_id =%s and b_id = %s;"
        cur.execute(sql,userPair)
        records = cur.fetchall()
        for r in records:
            VideoListForUser.append(list(r))
    except Exception:
        print(Exception)
    finally:
        conn.close()
    return VideoListForUser

def Vector(Userpairs):
    Vectors = []
    for pair in Userpairs:
        userVector =[]
        VideoList = getVideosForUser(pair)
        for video in VideoList:
            if video[2] ==1:
                #todo 查找其合并视频
            else:
                userVector.append(video[1])