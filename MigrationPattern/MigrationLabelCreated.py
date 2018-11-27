import pymysql
import traceback
import csv
import numpy
import pandas


'''
计算向量，给出迁移标签
'''
# row[0]-aid,row[1] bid,row[-1] length
# 计算用户向量长度
def vectorlength():
    Vectors =[]
    # 获取用户acfun向量
    with open('vector.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # 去除向量长度小于4的数据
            if len(row)>=6:
                row.append(len(row)-2)
                Vectors.append(row)
    print(Vectors)
    # 608个用户向量
    print(len(Vectors))
    tripletcount =0
    # 对于每一个用户
    for user in Vectors:
        # 仅仅向量两部分
        uservector = user[2:-1]
        print(uservector)
        usertripletcount = 0
        i = 0
        while i in range(0,len(uservector)-2):
            # 检查是否与下一个相同
            if uservector[i]==uservector[i+1]:
                # 相同
                if uservector[i] ==uservector[i+2]:
                    # 有连续三个相同的元素，i从第四个开始
                    usertripletcount+=1
                    i +=3
                else:
                    # 前两个相同，第三个不同,i从第三个开始
                    i +=2
            # 前两个不相同
            else:
                # i从第二个开始
                i+=1
        print(user[0],user[1])
        print(usertripletcount)
        tripletcount += usertripletcount

    print('共有三元组%d个'%tripletcount)
vectorlength()



#



