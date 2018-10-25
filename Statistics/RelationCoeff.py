#coding=utf8
import numpy as np
from pylab import *
import pymysql
import math
import os
mpl.rcParams['font.sans-serif'] =['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

'''
计算皮尔逊系数
'''
def PearsonCoeff(db):
    conn = pymysql.connect(host="127.0.0.1",user="root",passwd="root",charset="utf8")
    tuples=()
    if db =="acfun":
        sql="select playnum,bulletnum,commentnum,favoritenum from acfun_video where playnum >0;"
    else:
        sql = "select play,bullets,comment,favourites from bilibili_video_info where play >0;"
    '''
    计算B站皮尔逊系数
    '''
    try:
        conn.select_db(db)
        cur = conn.cursor()

        cur.execute(sql)
        tuples = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        pass
    playnum = []
    bulletnum =[]
    commentnum = []
    favnum = []
    for t in tuples:
        playnum.append(t[0])
        bulletnum.append(t[1])
        commentnum.append(t[2])
        favnum.append(t[3])

    dataarray= np.array((playnum,bulletnum,commentnum,favnum))
    #计算皮尔逊系数
    Pearson = np.corrcoef(dataarray)

    print(db+"皮尔逊系数矩阵：")
    print(Pearson)

'''
acfun皮尔逊系数矩阵：
[[  1.00000000e+00  -1.21448254e-04   8.18913017e-02   5.91210743e-02]
 [ -1.21448254e-04   1.00000000e+00  -1.36057732e-04   3.27156997e-03]
 [  8.18913017e-02  -1.36057732e-04   1.00000000e+00   3.18446019e-01]
 [  5.91210743e-02   3.27156997e-03   3.18446019e-01   1.00000000e+00]]
bilibili_whole皮尔逊系数矩阵：
[[ 1.          0.42213669  0.41229066  0.75650158]
 [ 0.42213669  1.          0.96434245  0.38595039]
 [ 0.41229066  0.96434245  1.          0.37189231]
 [ 0.75650158  0.38595039  0.37189231  1.        ]]
'''

'''
播放量累计分布图
'''

def PlaynumPerUserCDF():
    '''
    A 站数据
    '''
    conn = pymysql.connect(host="223.3.76.172",user="root",passwd="123",charset="utf8")
    tuples=()
    try:
        conn.select_db("bilibili")
        cur = conn.cursor()
        sql= "select totalplaynum from acfun_playnum;"
        cur.execute(sql)
        tuples = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()
    Atotalplaynum=[]
    for t in tuples:
        # Atotalplaynum.append(math.log(t[0],10))
        Atotalplaynum.append(t[0])
    #数据排序
    Atotalplaynum.sort()

    #计算数据比例 calculate the proportional values of samples，递增+1计数
    p1 = 100. * np.arange(1,len(Atotalplaynum)+1) / (len(Atotalplaynum))

    #B站数据
    conn = pymysql.connect(host="223.3.76.172",user="root",passwd="123",charset="utf8")
    tuples=()
    try:
        conn.select_db("bilibili")
        cur = conn.cursor()
        sql= "select playnum from bilibili_uppers_detail;"
        cur.execute(sql)
        tuples = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()
    Btotalplaynum=[]
    for t in tuples:
        if t[0]!=0:
            Btotalplaynum.append(t[0])
    #数据排序
    Btotalplaynum.sort()
    #计算数据比例 calculate the proportional values of samples，递增+1计数
    p2 = 100. * np.arange(1,len(Btotalplaynum)+1) / (len(Btotalplaynum))



    # plot the sorted data:
    #创建一个空figure
    fig = figure()

    plt.semilogx(Atotalplaynum, p1,'-',label='Acfun',color='k')  # x轴为对数坐标轴


    plt.semilogx(Btotalplaynum, p2,'--',label ='Bilibili',color='k')  # x轴为对数坐标轴



    plt.xlabel(u'单个用户视频播放量')
    plt.ylabel(u'累计百分比%')
    plt.title(u' Acfun/Bilibili单个用户播放量累计分布图')
    plt.savefig(u'PlaynumPerUserCDF.png')
    plt.legend()
    show()


'''
用户视频数量-频率双对数图
'''
def VideonumPerUserDoubleLog():
    '''
    A 站数据
    '''
    conn = pymysql.connect(host="127.0.0.1",user="root",passwd="root",charset="utf8")
    tuples=()
    try:
        conn.select_db("acfun")
        cur = conn.cursor()
        sql= "select videocount from upper_detail;"
        cur.execute(sql)
        tuples = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()
    Atotalplaynum=[]
    for t in tuples:
        Atotalplaynum.append(t[0])
    #数据排序
    Atotalplaynum.sort()
    #计算数据所占比例,存储某个数字在list中出现个数的字典
    p1 = []
    for a in Atotalplaynum:
        percentage= float(Atotalplaynum.count(a))/float(len(Atotalplaynum))
        p1.append(percentage)
    print(p1)

    #B站数据
    conn = pymysql.connect(host="127.0.0.1",user="root",passwd="root",charset="utf8")
    tuples=()
    try:
        conn.select_db("bilibili_whole")
        cur = conn.cursor()
        sql= "select videocount from upper_detail;"
        cur.execute(sql)
        tuples = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()
    Btotalplaynum=[]
    for t in tuples:
        Btotalplaynum.append(t[0])
    #数据排序
    Btotalplaynum.sort()

    #计算数据所占比例,存储某个数字在list中出现个数的字典
    p2 = []
    for a in Btotalplaynum:
        percentage= float(Btotalplaynum.count(a))/float(len(Btotalplaynum))
        p2.append(percentage)
    print(p2)

    # plot the sorted data:
    #创建一个空figure
    fig = figure()
    #一行二列的图像，选择第一个
    ax1 = fig.add_subplot(1,2,1)
    ax1.set_xlabel(u'单个用户上传视频数')
    ax1.set_ylabel(u'频率')
    plt.title(u' Acfun用户视频数量-频率双对数图')
    # ax1.semilogx(x, y)  # x轴为对数坐标轴
    # ax1.semilogy(x, y)  # y轴为对数坐标轴
    #
    ax1.loglog(Atotalplaynum, p1, linewidth=0)  # 双对数坐标轴
    ax1.scatter(Atotalplaynum, p1, s=10, color='black')

    # # 一行二列的图像，选择第二个
    ax2 = fig.add_subplot(1,2,2)

    ax2.set_xlabel(u'单个用户上传视频数')
    ax2.set_ylabel(u'频率')
    plt.title(u' Bilibili用户视频数量-频率双对数图')

    ax2.loglog(Btotalplaynum, p2, linewidth=0)  # 双对数坐标轴
    ax2.scatter(Btotalplaynum, p2, s=10, color='black')
    plt.show()

#
# PearsonCoeff("acfun")
# PearsonCoeff("bilibili_whole")
# VideonumPerUserDoubleLog()
PlaynumPerUserCDF()

