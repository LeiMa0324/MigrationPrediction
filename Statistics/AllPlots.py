#coding=utf8
import numpy as np
from pylab import *
import pymysql
from matplotlib import pyplot as plt

from matplotlib.font_manager import FontProperties  # 步骤一
import math
import os
import pandas as pd

#正常显示中文
# windows
font = FontProperties(fname='C:\Windows\Fonts\SimHei.ttf')
# mac
# font = FontProperties(fname='/Library/Fonts/Songti.ttc')
#正常显示负号
plt.rcParams['axes.unicode_minus'] = False



'''
计算皮尔逊系数
'''
def PearsonCoeff():
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    tuples=()
    '''
    计算B站皮尔逊系数
    '''
    try:
        conn.select_db("MigrationDetection02")
        cur = conn.cursor()
        # #二网重叠Acfun
        sql ='SELECT playnum,bulletnum,commentnum,favoritenum FROM overlap_acfun_videos;'
        # 二网重叠Bili
        # sql = "SELECT play,bullets,comment,favourites FROM overlap_bili_videos;"
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
    print(dataarray)
    #计算皮尔逊系数
    Pearson = np.corrcoef(dataarray)

    print('#二网重叠Acfun')
    # print("二网重叠用户-Bilibili皮尔逊系数矩阵：")
    print(Pearson)


PearsonCoeff()

'''
第三章 图3.3播放量累计分布图
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

    plt.semilogx(Atotalplaynum, p1,'-',label='Acfun',color='k')  # x轴为对数坐标轴
    plt.semilogx(Btotalplaynum, p2,'--',label ='Bilibili',color='k')  # x轴为对数坐标轴

    plt.xlabel(u'单个用户视频播放量')
    plt.ylabel(u'累计百分比%')
    plt.title(u' Acfun/Bilibili单个用户播放量累计分布图')
    plt.savefig(u'PlaynumPerUserCDF.png')
    plt.legend()
    show()


'''
第三章 图3.2用户视频数量-频率双对数图
'''
def VideonumPerUserDoubleLog():
    '''
    A 站数据
    '''
    conn = pymysql.connect(host="223.3.76.172",user="root",passwd="123",charset="utf8")
    tuples=()
    try:
        conn.select_db("bilibili")
        cur = conn.cursor()
        sql= "select videocount from acfun_uppers_detail;"
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
    conn = pymysql.connect(host="223.3.76.172",user="root",passwd="123",charset="utf8")
    tuples=()
    try:
        conn.select_db("bilibili")
        cur = conn.cursor()
        sql= "select videocount from bili_video_count;"
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

    #创建一个空figure
    fig = figure()
    #一行二列的图像，选择第一个
    ax1 = fig.add_subplot(1,2,1)
    ax1.set_xlabel(u'单个用户上传视频数')
    ax1.set_ylabel(u'频率')
    plt.title(u' Acfun用户视频数量-频率双对数图')
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



'''
第四章 图4.4 common video-频率双对数图
'''
def CommonVideoDoubleLog():
    '''
    A 站数据
    '''
    conn = pymysql.connect(host="223.3.76.172",user="root",passwd="123",charset="utf8")
    tuples=()
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        sql= "SELECT common_videos FROM MigrationDetection01.UsermappingByVideo; "
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


    # plot the sorted data:

    #一行二列的图像，选择第一个
    plt.xlabel(u'Acfun-Bilibili两用户之间相同视频数',fontproperties =font)
    plt.ylabel(u'频率',fontproperties ="SimHei")
    plt.title(u' Acfun-Bilibili用户相同视频数量-频率双对数图',fontproperties ="SimHei")

    plt.loglog(Atotalplaynum, p1, linewidth=0)  # 双对数坐标轴
    plt.scatter(Atotalplaynum, p1, s=10, color='black')

    plt.show()

'''
第四章 图4.5 相同视频数累计分布图
'''
def CommonVideoCDF():
    '''
    A 站数据
    '''
    conn = pymysql.connect(host="223.3.76.172",user="root",passwd="123",charset="utf8")
    tuples=()
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        sql= "select common_videos from UsermappingByVideo where common_videos>1;"
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
    print(Atotalplaynum)

    #计算数据比例 calculate the proportional values of samples，递增+1计数
    p1 = 100. * np.arange(1,len(Atotalplaynum)+1) / (len(Atotalplaynum))

    plt.semilogx(Atotalplaynum, p1,'-',label='Acfun',color='k')  # x轴为对数坐标轴
    plt.xlabel(u'相同视频数',fontproperties =font)
    plt.ylabel(u'累计百分比%',fontproperties =font)
    plt.title(u' Acfun/Bilibili用户相同视频数累计分布图',fontproperties =font)
    plt.savefig(u'CommonVideoCDF.png')
    show()

'''
第四章 图4.6 比例散点图
'''
def percentScatter():

    conn = pymysql.connect(host="223.3.76.172",user="root",passwd="123",charset="utf8")
    records=()
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        sql= "SELECT a_percent,b_percent,found FROM MigrationDetection01.UsermappingByVideo; "
        cur.execute(sql)
        records = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()
    percent_a = []
    percent_b = []
    label = []
    for row in records:
        percent_a.append(row[0])
        percent_b.append(row[1])
        label.append((row[2]))

    # 绘制散点图
    plt.xlabel(u'占A站视频的比例',fontproperties =font)
    plt.ylabel(u'占B站视频的比例',fontproperties =font)
    plt.title(u' ',fontproperties =font)
    plt.scatter(percent_a,percent_b,s=20,c=label)
    plt.show()



'''
第四章 图4.7 Levenshtein散点图
'''
# 计算Levenshtein距离
def LevenshteinDistStastic():
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    records=()
    LevenDist =[]
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        sql = "SELECT LevenDist FROM MigrationDetection01.UsermappingByVideo order by common_videos desc limit 250;"
        cur.execute(sql)
        records = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()

    LevenDist =[]

    # 对每一个levendist计数
    for r in records:
        LevenDist.append(r[0])

    LevenDist.sort()
    count =[]
    label = []
    for Leven in LevenDist:
        count.append(LevenDist.count(Leven))


    # 绘制散点图
    plt.xlabel(u'Acfun-Bilibili用户名Levenshtein比例',fontproperties =font)
    plt.ylabel(u'出现次数',fontproperties =font)
    plt.title(u' ',fontproperties =font)
    plt.scatter(LevenDist,count,s=20)
    plt.show()


'''
第四章 图4.8 A/B上传视频散点图
'''
# 计算Levenshtein距离
def VideosComparasion():
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    records=()
    LevenDist =[]
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        sql = "SELECT a_videos,b_videos FROM MigrationDetection01.overlapping_final order by a_videos;"
        cur.execute(sql)
        records = cur.fetchall()
    except Exception:
        print(Exception)
    finally:
        conn.close()

    a_videos = []
    b_videos = []


    for r in records:
        a_videos.append(r[0])
        b_videos.append(r[1])



    # 绘制散点图
    plt.xlabel(u'重叠用户编号',fontproperties =font)
    plt.ylabel(u'用户上传视频数量',fontproperties =font)
    plt.title(u' ',fontproperties =font)
    # PPT用图
    # plt.scatter(range(1,len(a_videos)+1),a_videos,s=10,alpha=0.5,label='Acfun')
    # plt.scatter(range(1,len(a_videos)+1),b_videos,s=10,alpha=0.5,label ='Bilibili')
    # 论文用图
    plt.scatter(range(1,len(a_videos)+1),a_videos,s=15,marker='*',label='Acfun',c='',edgecolors='k')
    plt.scatter(range(1,len(a_videos)+1),b_videos,s=10,marker='o',label ='Bilibili',c='',edgecolors='k')
    plt.legend(loc=2)
    plt.show()

'''
第四章 图5.2 同一个视频上传时间差直方图
'''
def TimeDiffHist():
    data =[]
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        sql = 'SELECT time_diff FROM MigrationDetection01.synthetic_videos;'
        cur.execute(sql)
        records = cur.fetchall()
        for r in records:
            data.append(int(r[0]))

    except Exception:
        print(Exception)

    finally:
        conn.close()


    """
    绘制直方图
    data:必选参数，绘图数据
    bins:直方图的长条形数目，可选项，默认为10
    normed:是否将得到的直方图向量归一化，可选项，默认为0，代表不归一化，显示频数。normed=1，表示归一化，显示频率。
    facecolor:长条形的颜色
    edgecolor:长条形边框的颜色
    alpha:透明度
    """
    print(data)
    plt.hist(data,range=(-2,10),facecolor='steelblue', edgecolor="black",label='频数',alpha=0.5,
             )
    # 显示横轴标签
    plt.xlabel("用户在Acfun和Bilibili发布同一视频的时间差/天",fontproperties =font)
    # 显示纵轴标签
    plt.ylabel("频数",fontproperties =font)
    # 显示图标题
    # plt.title("同一视频在Acfun和Bilibili的上传时间差频数图",fontproperties =font)
    plt.grid(True)
    plt.legend(prop =font)
    plt.show()


