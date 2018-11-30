import csv
import pandas as pd
import numpy as np

class User(object):
    aid =''
    bid =''
    states =[]
    vector =[]
    laststate = ''

    # 'A''B''S''U'出现次数
    anum = 0
    bnum = 0
    snum = 0
    unum = 0

    #'转移出现次数'
    aanum =0
    abnum =0
    asnum =0
    aunum =0

    banum =0
    bbnum =0
    bsnum =0
    bunum =0

    sanum =0
    sbnum =0
    ssnum =0
    sunum =0

    uanum =0
    ubnum =0
    usnum =0
    uunum =0


    # 初始化
    def __init__(self,aid,bid,states):
        self.aid = aid
        self.bid = bid
        self.states = states
        self.laststate = self.states[-1]
        anum = self.states.count('A')
        bnum = self.states.count('B')
        snum = self.states.count('S')
        unum = self.states.count('U')

        if self.laststate=='A':
            anum = anum-1
        elif self.laststate =='B':
            bnum = bnum-1
        elif self.laststate =='S':
            snum = snum-1
        elif self.laststate =='U':
            unum = unum-1

        # 统计出现次数
        self.anum = anum
        self.bnum = bnum
        self.snum = snum
        self.unum = unum

        return

    def getstates(self):
        return self.states

    def getids(self):
        return [self.aid,self.bid]

    def getstatescount(self):
        return [self.anum,self.bnum,self.snum,self.unum]

    def transfromA(self):
        return [self.aanum,self.abnum,self.asnum,self.aunum]

    def transfromB(self):
        return [self.banum,self.bbnum,self.bsnum,self.bunum]

    def transfromS(self):
        return [self.sanum,self.sbnum,self.ssnum,self.sunum]

    def transfromU(self):
        return [self.uanum,self.ubnum,self.usnum,self.uunum]

    def twoTuplesCount(self):
        aindex =[]
        bindex =[]
        sindex =[]
        uindex =[]
        for i in range(0,len(self.states)):
            if self.states[i] =='A':
                aindex.append(i)
            elif self.states[i]=='B':
                bindex.append(i)
            elif self.states[i]=='S':
                sindex.append(i)
            elif self.states[i]=='U':
                uindex.append(i)


        for a in aindex:
            if a != len(self.states)-1:
                tostate = self.states[a+1]
                if tostate =='A':
                    self.aanum +=1
                elif tostate =='B':
                    self.abnum +=1
                elif tostate =='S':
                    self.asnum +=1
                elif tostate =='U':
                    self.aunum +=1

        for b in bindex:
            if b != len(self.states)-1:
                tostate = self.states[b+1]
                if tostate =='A':
                    self.banum +=1
                elif tostate =='B':
                    self.bbnum +=1
                elif tostate =='S':
                    self.bsnum +=1
                elif tostate =='U':
                    self.bunum +=1

        for s in sindex:
            if s != len(self.states)-1:
                tostate = self.states[s+1]
                if tostate =='A':
                    self.sanum +=1
                elif tostate =='B':
                    self.sbnum +=1
                elif tostate =='S':
                    self.ssnum +=1
                elif tostate =='U':
                    self.sunum +=1

        for u in uindex:
            if u != len(self.states)-1:
                tostate = self.states[u+1]
                if tostate =='A':
                    self.uanum +=1
                elif tostate =='B':
                    self.ubnum +=1
                elif tostate =='S':
                    self.usnum +=1
                elif tostate =='U':
                    self.uunum +=1



# 获取用户状态序列
def getStates():
    states =[]
    with open('states_2_networks.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            states.append(row)

    return states


states = getStates()
#A,B,S,U各自出现的次数
globalstatenum = np.array([0,0,0,0])
# 从A 转移到其他状态的个数
globaltransFromA = np.array([0,0,0,0])
# 从B 转移到其他状态的个数
globaltransFromB = np.array([0,0,0,0])
# 从S 转移到其他状态的个数
globaltransFromS = np.array([0,0,0,0])
# 从U 转移到其他状态的个数
globaltransFromU = np.array([0,0,0,0])




for s in states:
    user = User(s[0],s[1],s[2:])
    user.twoTuplesCount()
    print('--------------------------------------------')
    print('用户名')
    print(user.getids())
    print(user.getstates())

    userstatenum = np.array(user.getstatescount())
    print('全局次数')
    print(globalstatenum)
    print('用户共出现的状态计数')
    print(userstatenum)
    globalstatenum +=userstatenum
    print('update后的全局次数')
    print(globalstatenum)

    print('全局转移')
    print(globaltransFromA)
    print(globaltransFromB)
    print(globaltransFromS)
    print(globaltransFromU)

    print('用户状态转移矩阵')
    print(user.transfromA())
    print(user.transfromB())
    print(user.transfromS())
    print(user.transfromU())

    globaltransFromA += np.array(user.transfromA())
    globaltransFromB +=np.array(user.transfromB())
    globaltransFromS +=np.array(user.transfromS())
    globaltransFromU +=np.array(user.transfromU())

    print('update后的全局转移')
    print(globaltransFromA)
    print(globaltransFromB)
    print(globaltransFromS)
    print(globaltransFromU)





print('全局统计结果')
print('state次数')
print(globalstatenum)
print('转移次数')
print(globaltransFromA)
print(globaltransFromB)
print(globaltransFromS)
print(globaltransFromU)

globaltransProbFromA = globaltransFromA/globalstatenum[0]
globaltransProbFromB = globaltransFromB/globalstatenum[1]
globaltransProbFromS = globaltransFromS/globalstatenum[2]
globaltransProbFromU = globaltransFromU/globalstatenum[3]

print('全局转移概率矩阵')
print(globaltransProbFromA)
print(globaltransProbFromB)
print(globaltransProbFromS)
print(globaltransProbFromU)

df = pd.DataFrame(columns=['A','B','S','U'])
df.loc[0] = globaltransProbFromA
df.loc[1] = globaltransProbFromB
df.loc[2] = globaltransProbFromS
df.loc[3] = globaltransProbFromU

print(df)
df.to_csv('globalTransProb_2_networks.csv')

'''
1. 无论A站还是B站，短期内都倾向于忠于一个网站
2. 相比较A站，B站的用户忠实度更高
2. 同步用户在短期内倾向于继续同步
3. 处于不稳定的用户，下一步大概率将转移到B站

3. 较为明显的迁移趋势排序为
    1.A->U->B
    2.B->B
    3.S->U->B
    4.U->B
'''