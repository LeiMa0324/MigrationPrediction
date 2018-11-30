import pymysql
import traceback
import csv
import numpy
import pandas


'''
计算向量，给出迁移标签
'''

# 计算m=3时用户向量长度
def vectorlength():
    Vectors = getVectors()
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



# 获取用户向量
def getVectors():
    rows =[]
    Vectors =[]

    # 获取用户acfun向量
    with open('vector_2_networks.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # 去除向量长度小于4的数据
            if len(row)>=6:
                rows.append(row)
    print(rows)

    for r in rows:
        uservector =[]
        uservector.append(r[0])
        uservector.append(r[1])
        for i in range(2,len(r)):
            newpair = [int(r[i][1]),int(r[i][4])]

            uservector.append(newpair)
        Vectors.append(uservector)

    print(Vectors)
    return Vectors





class User(object):

    aid =''
    bid=''
    states =[]
    vector =[]
    laststateindex = 0

    # 初始化
    def __init__(self,aid,bid,vector):
        self.aid = aid
        self.bid = bid
        self.vector = vector
        self.states = []
        self.laststateindex = 0

    def getstates(self):
        return self.states

    def writestates(self):
        content =[self.aid,self.bid]
        content.extend(self.states)
        with open('states_2_networks.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(content)


    def getids(self):
        return [self.aid,self.bid]

    def getvectors(self):
        return self.vector

    def getlaststateindex(self):
        return self.laststateindex

    def updatelaststateindex(self,l):
        self.laststateindex=l

    # 检查是否需要插入Unstable状态
    def isNeedUnstable(self,i):
        if i- self.laststateindex>1:
            return self.states.append('U')
        else:
            return

    # 判断状态类型
    def stateClassifier(self,element):
        if element == [1,0]:
            return self.states.append('A')
        elif element == [0,1]:
            return self.states.append('B')
        elif element == [1,1]:
            return self.states.append('S')

    # 插入stable状态
    def stablestateInsert(self,i):
        # 是否需要插入unstable
        self.isNeedUnstable(i)
        # 判断状态类型并插入状态
        self.stateClassifier(self.vector[i])
        # 更新laststateindex
        self.laststateindex = i+1
        return

    def slidingwindow(self):
        i = 0
        while i <len(self.vector):
            # i最大为倒数第三个数
            if i <len(self.vector)-2:
                # i与i+1相等
                if self.vector[i] == self.vector[i+1]:
                    self.stablestateInsert(i)
                    i +=2
                # i与i+1不相等
                else:
                    i +=1
            # i为倒数第二个数
            elif i == len(self.vector)-2:
                # 倒数第二与倒数第一相同
                if self.vector[i] == self.vector[i+1]:
                    self.stablestateInsert(i)
                    break
                # 倒数第二与倒数第一不同
                else:
                    self.states.append('U')
                    break
            # 倒数第一位，检查是否需要插入U
            elif i == len(self.vector)-1:
                self.isNeedUnstable(i)
                break

Vectors = getVectors()

Userlist =[]
for vec in Vectors:
    user = User(vec[0],vec[1],vec[2:-1])
    Userlist.append(user)

for i in range(0,len(Userlist)):
    Userlist[i].slidingwindow()
    print(Userlist[i].getids())
    print(Userlist[i].getvectors())
    print(Userlist[i].getstates())
    Userlist[i].writestates()




