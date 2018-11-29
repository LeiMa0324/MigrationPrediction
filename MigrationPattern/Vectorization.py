import pymysql
import traceback
import csv


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

# 查找某个视频对应的同步视频
def getSyntheticVideo(vid,abFlag):

    syntheticVid=''
    if abFlag =='A':
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection02")
            cur = conn.cursor()
            sql = "SELECT b_vid FROM MigrationDetection02.close_updates where a_vid = %s;"
            cur.execute(sql, vid)
            syntheticVid = cur.fetchone()[0]
        except Exception:
            print(Exception)
        finally:
            conn.close()
    else:
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection02")
            cur = conn.cursor()
            sql = "SELECT a_vid FROM MigrationDetection02.close_updates where b_vid = %s;"
            cur.execute(sql, vid)
            syntheticVid = cur.fetchone()[0]
        except Exception:
            print(Exception)
        finally:
            conn.close()
    reverseFlag = ('A' if abFlag=='B' else 'B')
    return [syntheticVid,reverseFlag]

# 插入序列到数据库
def insertVectors(Vec_element):
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    try:
        conn.select_db("MigrationDetection02")
        cur = conn.cursor()
        sql = "INSERT INTO `MigrationDetection02`.`overlap_vectors`(a_id,b_id,vec_element) values (%s,%s,%s);"
        cur.executemany(sql, Vec_element)
        conn.commit()
        print('insert sucessed!')
    except Exception as err:
        print(err)
        print(traceback.print_exc())
    finally:
        conn.close()

# 获取abFlag序列
def FlagSeriesExtraction(Userpairs):
    i = 0
    # 对于每一对重叠用户
    for pair in Userpairs:
        print('处理第%d个用户...'% i)
        # 用户行为向量
        userVector = []
        # 需要删除的位数
        deletevideos = []
        # 获取用户视频
        VideoList = getVideosForUser(pair)
        for video in VideoList:
            ele = []
            print([video[0], video[1]])
            # 判断当前video是否属于需要被删除的视频
            if [video[0], video[1]] in deletevideos:
                print('synthetic video, delete item...')
                continue
            else:
                # 该视频存在closeupdate
                if video[2] == 1:

                    # 如果该视频为Acfun上传的视频，查找其在B站的视频
                    [syntheticVid, reverseFlag] = getSyntheticVideo(video[0], video[1])
                    # 将同步视频存入delevideos
                    deletevideos.append([syntheticVid, reverseFlag])
                    print('video %s has synthetic video, add it to delete list.' % video[0])

                    ele.extend(pair)
                    ele.append('AB')
                    print(ele)
                    userVector.append(ele)

                else:
                    ele.extend(pair)
                    ele.append(video[1])

                    userVector.append(ele)
        print("该用户向量长度%d，被删除位数%d" % (len(userVector), len(deletevideos)))
        print(userVector)

        # 插入数据库
        insertVectors(userVector)
        i+=1

def vector():
    UserPairs = getUserPairs()
    # 对于每一对重叠用户
    for pair in UserPairs:
        Series =[]
        acVector = []
        acVector.extend(pair)
        biliVector = []
        biliVector.extend(pair)
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection02")
            cur = conn.cursor()
            sql = "SELECT vec_element FROM MigrationDetection02.overlap_vectors where a_id=%s and b_id=%s;"
            cur.execute(sql,pair)
            records = cur.fetchall()
            for row in records:
                Series.append(row[0])
        except Exception as err:
            print(err)
            print(traceback.print_exc())
        finally:
            conn.close()

        print(Series)
        # 对每一个标记
        for s in Series:
            # 标签为‘A’，ac向量记1，bili记0
            if s =='A':
                acVector.append('1')
                biliVector.append('0')
            else:
                # 标签为‘B’，ac向量记0，bili记1
                if s=='B':
                    acVector.append('0')
                    biliVector.append('1')
                    # 标签为'AB',同时记1
                else:
                    acVector.append('1')
                    biliVector.append('1')


        with open('acfun_vectors.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(acVector)

        with open('bili_vectors.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(biliVector)


def vector01():
    UserPairs = getUserPairs()
    # 对于每一对重叠用户
    for pair in UserPairs:
        Series =[]
        Vector = []
        Vector.extend(pair)

        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection02")
            cur = conn.cursor()
            sql = "SELECT vec_element FROM MigrationDetection02.overlap_vectors where a_id=%s and b_id=%s;"
            cur.execute(sql,pair)
            records = cur.fetchall()
            for row in records:
                Series.append(row[0])
        except Exception as err:
            print(err)
            print(traceback.print_exc())
        finally:
            conn.close()

        print(Series)
        # 对每一个标记
        for s in Series:
            # 标签为‘A’，ac向量记1，bili记0
            if s =='A':
                Vector.append([1,0])

            else:
                # 标签为‘B’，ac向量记0，bili记1
                if s=='B':
                    Vector.append([0,1])

                    # 标签为'AB',同时记1
                else:
                    Vector.append([1,1])


        with open('vector.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(Vector)

vector01()