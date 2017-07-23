#coding=utf8
import numpy as np
from pylab import *
import scikits.statsmodels as sm
import pymysql
import math
import os
mpl.rcParams['font.sans-serif'] =['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

'''
计算皮尔逊系数
'''
def PearsonCoeff():
    conn = pymysql.connect(host="127.0.0.1",user="root",passwd="root",charset="utf8")
    tuples=()
    try:
        conn.select_db("acfun")
        cur = conn.cursor()
        sql= "select playnum,bulletnum from acfun_video where playnum >0;"
        cur.execute(sql)
        tuples = cur.fetchall()
    except Exception,e:
        print e
    finally:
        conn.close()
    playnum=[]
    bulletnum =[]
    for t in tuples:
        playnum.append(t[0])
        bulletnum.append(t[1])

    PlayAndBullet = np.array((playnum,bulletnum))
    #计算皮尔逊系数
    PandBCoeff = np.corrcoef(PlayAndBullet)
    #计算协方差矩阵
    PandBCoeff = np.cov(PlayAndBullet)
    print PandBCoeff
    #结论：视频点击率与弹幕数不成正比

'''
绘制累计分布图
'''
def CDFPlot():
    '''
    A 站数据
    '''
    conn = pymysql.connect(host="127.0.0.1",user="root",passwd="root",charset="utf8")
    tuples=()
    try:
        conn.select_db("acfun")
        cur = conn.cursor()
        sql= "select total_playnum from upper_detail;"
        cur.execute(sql)
        tuples = cur.fetchall()
    except Exception,e:
        print e
    finally:
        conn.close()
    Atotalplaynum=[]
    for t in tuples:
        Atotalplaynum.append(math.log(t[0],10))
    #数据排序
        Atotalplaynum.sort()
    #计算数据比例 calculate the proportional values of samples，递增+1计数
    p1 = 100. * np.arange(1,len(Atotalplaynum)+1) / (len(Atotalplaynum))

    #B站数据
    conn = pymysql.connect(host="127.0.0.1",user="root",passwd="root",charset="utf8")
    tuples=()
    try:
        conn.select_db("bilibili_whole")
        cur = conn.cursor()
        sql= "select playnum from uppers_detail;"
        cur.execute(sql)
        tuples = cur.fetchall()
    except Exception,e:
        print e
    finally:
        conn.close()
    Btotalplaynum=[]
    for t in tuples:
        if t[0]!=0:
            Btotalplaynum.append(math.log(t[0],10))
    #数据排序
        Btotalplaynum.sort()
    #计算数据比例 calculate the proportional values of samples，递增+1计数
    p2 = 100. * np.arange(1,len(Btotalplaynum)+1) / (len(Btotalplaynum))



    # plot the sorted data:
    #创建一个空figure
    fig = figure()
    #一行二列的图像，选择第一个
    ax1 = fig.add_subplot(1,2,1)
    ax1.plot(Atotalplaynum,p1)
    ax1.set_xlabel(u'播放量/每个用户(log10)')
    ax1.set_ylabel(u'累计百分比%')
    plt.title(u' Acfun用户播放量累计分布图')

    # # 一行二列的图像，选择第二个
    ax2 = fig.add_subplot(1,2,2)
    ax2.plot(Btotalplaynum, p2)
    ax2.set_xlabel(u'播放量/每个用户(log10)')
    ax2.set_ylabel(u'累计百分比%')
    plt.title(u' Bilibili用户播放量累计分布图')

    plt.plot()
    show()
    savefig("CDF.png")


CDFPlot()

