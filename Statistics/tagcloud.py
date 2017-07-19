# -*- coding: utf-8 -*-
import pytagcloud
import pymysql
import matplotlib
from matplotlib import pylab
import  random
from pylab import mpl
from pytagcloud import create_tag_image, create_html_data, make_tags, \
    LAYOUT_HORIZONTAL, LAYOUTS
from pytagcloud.colors import COLOR_SCHEMES
mpl.rcParams['font.sans-serif'] =['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

#wordcounts 是一个列表，元素是元组
'''
绘制云标签图片
'''
def tagcloud():
    conn = pymysql.connect(host="127.0.0.1",user="root",passwd ="root",charset="utf8") \

    wordcounts = []
    try:
        cur = conn.cursor()
        conn.select_db("bilibili_whole")
        # sql="select tagName,refCount from acfun_tag order BY  refCount desc limit 150;"
        sql="select tagname,taguse from bilibili_tags order BY  taguse desc limit 150"
        cur.execute(sql)
        tuples = list(cur.fetchall())
        tuples.pop(0)
    except Exception,e:
        print e
    finally:
        conn.close()
    for t in tuples:
        wordcounts.append((t[0],int(t[1])))
    print wordcounts
    tags = pytagcloud.make_tags(wordcounts,minsize=30,maxsize=240,colors=random.choice(COLOR_SCHEMES.values()))
    print tags
    pytagcloud.create_tag_image(tags, 'bili_tag_cloud.png', size=(2400, 1000),background=(0, 0, 0, 255),layout=LAYOUT_HORIZONTAL,fontname="SimHei")

tagcloud()