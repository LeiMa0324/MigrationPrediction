from sklearn.linear_model import LogisticRegression
from sklearn import datasets
import pymysql
import numpy as np
import Levenshtein
import difflib
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties  # 步骤一
import re
import csv

font = FontProperties(fname='C:\Windows\Fonts\SimHei.ttf')
'''
学习common_percent_a和common_percent_b对于重叠用户的模型
使用logistic
'''


# 获取common videos占重叠用户发布的视频百分比
def dataretieve():
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    records = ()
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        sql = "SELECT common_percent_a,common_percent_b FROM MigrationDetection01.UsermappingByVideo where found=1; "
        cur.execute(sql)
        records = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()

    recordList = []
    # 转化为list
    for row in records:
        new_row = list(row)
        recordList.append(new_row)

    return recordList

def LogisticModel(records):

    loaded_data = datasets.load_boston()
    data_X = loaded_data.data
    data_y = loaded_data.target

    print(data_X.shape)
    # '''
    # 归一化Normailization:将特征通过最大最小值，缩放到[0,1]之间
    # 标准化standardization：将特征值缩放为一个标准正态分布，均值为0，方差为1
    # '''
    # std = StandardScaler()
    # data_X_std = std.fit_transform(data_X)
    #
    # '''
    # 选择一个模型
    # model.fit(X_train,y_train)即为学习
    # model.predict(X_test)即为预测
    # '''
    # model = LinearRegression()
    # model.fit(data_X, data_y)
    # '''
    # model的属性和功能
    # '''
    # # 输出参数(weights)
    # print(model.coef_)  # y = 0.1x+0.3
    # # 输出截距(bias)
    # print(model.intercept_)
    # # 返回调用LinearRegression时的参数值，不填则为默认
    # print(model.get_params())
    # # 返回R^2 COEFFICIENT OF DETERMINATION 决定系数
    # print(model.score(data_X, data_y))


# 计算Levenshtein距离
def LevenshteinDist():
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    records = ()
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        sql = "SELECT a_username,b_name FROM MigrationDetection01.UsermappingByVideo;"
        cur.execute(sql)
        records = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()


    for row in records:
        # 4.计算莱文斯坦比
        # 计算公式  r = (sum - ldist) / sum, 其中sum是指str1 和 str2 字串的长度总和，ldist是 类编辑距离
        sim = Levenshtein.ratio(row[0], row[1])
        print(row[0],row[1])
        print('Levenshtein.ratio similarity: ', sim)
        newrow = [sim,row[0],row[1]]
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection01")
            cur = conn.cursor()
            sql = "update MigrationDetection01.UsermappingByVideo set LevenDist =%f "%sim
            sql += 'where a_username=%s and b_name=%s;'

            cur.execute(sql,(row[0],row[1]))

        except Exception:
            print(Exception)
        finally:
            conn.commit()
            conn.close()




# 合并三张表，找出最后的重叠用户
def OverlappingFinal():

    overlapping = []

    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    records= ()
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        sql = "SELECT a_id,b_id,weibo_id,weibo_name,weibo_realm FROM MigrationDetection01.overlapping_final01;"
        cur.execute(sql)
        records = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()

    for row in records:
        new_row = list(row)
        if new_row not in overlapping:
            overlapping.append(new_row)

    print(overlapping)
    print(len(overlapping))

    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        sql = "insert into overlapping_final02(a_id,b_id,weibo_id,weibo_name,weibo_realm) values(%s,%s,%s,%s,%s);"
        cur.executemany(sql,overlapping)
        conn.commit()
    except Exception:
        print(Exception)

    finally:
        conn.close()



overlapping = []

conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
records= ()
try:
    conn.select_db("MigrationDetection01")
    cur = conn.cursor()
    sql = "SELECT b_id FROM MigrationDetection01.overlapping_final  where b_videos is null;"
    cur.execute(sql)
    records = cur.fetchall()
except Exception:
    print(Exception)
finally:
    conn.close()

for row in records:
    new_row = list(row)
    overlapping.append(new_row)
print(overlapping)

videocount  =[]
conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
try:
    conn.select_db("MigrationDetection01")
    cur = conn.cursor()
    sql = "SELECT mid,count(*) FROM MigrationDetection01.bili_video_addup where mid =%s;"
    for user in overlapping:
        cur.execute(sql,user)
        count = cur.fetchone()
        if count[0] !=None:
            videocount.append(list(count))


except Exception:
    print(Exception)

finally:
    conn.close()

print(videocount)

conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
try:
    conn.select_db("MigrationDetection01")
    cur = conn.cursor()
    sql = "update overlapping_final set b_videos = %s where b_id =%s;"
    for i in videocount:
        cur.execute(sql,(i[1],i[0]))

    conn.commit()
except Exception:
    print(Exception)

finally:
    conn.close()