from sklearn.linear_model import LogisticRegression
from sklearn import datasets
import pymysql
import numpy as np


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

LogisticModel()