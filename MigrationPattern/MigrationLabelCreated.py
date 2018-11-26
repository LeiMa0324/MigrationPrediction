import pymysql
import traceback
import csv


'''
计算向量，给出迁移标签
'''
# 计算用户向量长度
def vectorlength():
    userVectors =[]
    with open('acfun_vectors.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            userVectors.append(row)
            print(len(row))
    print(userVectors)
    #todo 去除向量长度太短的数据

vectorlength()