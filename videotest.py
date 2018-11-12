# coding=utf-8

import requests
import json
import random
import pymysql
from multiprocessing.dummy import Pool as ThreadPool
import sys
import datetime
import time
from imp import reload
import traceback,sys
from requests.exceptions import ProxyError
import urllib
import math




head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
}

#?mid=20779567&pagesize=30&tid=0&page=1&keyword=&order=senddate

'''
返回的是当页的 video，并不是所有的,
需要做一个 for 循环遍历所有 page
'''
#发送请求
def VideoRequest(mid,pagenum):
    payload={
    'mid':mid,
    'pagesize':'100',
    'tid':'0',
    'page':pagenum,
    'keyword':'',
    'order':'senddate'}
    url='http://space.bilibili.com/ajax/member/getSubmitVideos'

    VideoRequestList=[]
    #发送请求
    videocJson = requests.get(url,params=payload, headers=head).content
    print(videocJson)

    avDict = json.loads(videocJson)
    #校验Json数据
    statusJson = avDict['status'] if 'status' in avDict.keys() else False
    if statusJson == True:
        #json中有数据
        if 'data' in avDict.keys():
            #每一页的视频列表与视频总个数
            if avDict['data']['count']>0:
                VideoRequestList.append(avDict['data']['count'])
                VideoRequestList.append(avDict['data']['vlist'])
                return VideoRequestList
            else:
                print("该用户视频数为0")
        else:
            print('no data')
    else:
        print('NoJson')



#返回某个用户的所有视频列表
def GetVideoSource(mid):
    pagecount=0
    pagenum=1
    #视频分页列表，其中每一项都是每一页的视频列表
    VideoPageAllList=[]
    #视频分条列表
    VideoList=[]
    #请求第一页
    VideoPageOneList=VideoRequest(mid,str(pagenum))

    if VideoPageOneList!=None:
        VideoPageAllList.append(VideoPageOneList[1])
        #获取总页数
        pagecount=math.ceil(int(VideoPageOneList[0])/100.0)
        #遍历所有页
        while pagenum!=pagecount:
            pagenum +=1
            VideoPageAllList.append(VideoRequest(mid,pagenum)[1])
        #整理video数据
        for i in range(0,len(VideoPageAllList)):
            for j in range(0,len(VideoPageAllList[i])):
                VideoList.append(VideoPageAllList[i][j])
        print("获取用户%s共视频%s条" %(mid,len(VideoList)))
        InsertTagsandVideo2DB(VideoList)

    else:
        print("该用户%s没有视频数据"% mid)



#视频数据和tag插入数据库
def InsertTagsandVideo2DB(VideoListlocal):
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset='utf8')

    try:
        cur = conn.cursor()
        conn.select_db("bilibili")
        #插入视频数据
        sql="INSERT INTO bili_video_addup(aid, comment,copyright,created,favourites,length,mid,play,review,title,typeid,video_review) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        tmp=[]
        for i in range(0, len(VideoListlocal)):
            data = [VideoListlocal[i]['aid'],VideoListlocal[i]['comment'],VideoListlocal[i]['copyright'],VideoListlocal[i]['created'],VideoListlocal[i]['favorites'],
                 VideoListlocal[i]['length'],VideoListlocal[i]['mid'],VideoListlocal[i]['play'],VideoListlocal[i]['review'],VideoListlocal[i]['title'],
                 VideoListlocal[i]['typeid'],VideoListlocal[i]['video_review']]
            tmp.append(data)
        cur.executemany(sql,tmp)
        # conn.commit()
        print("用户：%s视频：%s条已存入数据库" %(VideoListlocal[0]['mid'],len(VideoListlocal)))

        conn.commit()
        cur.close()
    except Exception:
        print(Exception)
    finally:
        conn.close()


# 主程序
conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset='utf8',db='bilibili')
sql = "SELECT b_id FROM bilibili.neighbour where b_id!='NULL'";
cur = conn.cursor()
cur.execute(sql)
record = cur.fetchall()
for r in record:
    GetVideoSource(r)

