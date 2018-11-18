# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mBox
import pymysql


win = tk.Tk()
win.title(u"多网络重叠用户迁移预测系统")
scnWidth,scnHeight = win.maxsize()
tmpcnf = '%dx%d+%d+%d'%(785, 537, (scnWidth-785)/2, (scnHeight-537)/2)
win.geometry(tmpcnf)


#=============================================================
#模块创建
#=============================================================
data = ttk.LabelFrame(win, text=u'选择重叠用户')
data.grid(column=0,row=0,rowspan=1,padx=20,pady=20,ipadx=10,sticky=tk.W)

similarity = ttk.LabelFrame(win, text=u'用户信息')
similarity.grid(column=0, row=1,rowspan=1,padx=20,pady=20,ipadx=10,sticky=tk.W)

network= ttk.LabelFrame(win,text=u'用户迁移预测')
network.grid(column=1, row=1,padx=20,pady=30,ipadx=20)



#----------------------------UI区-----------------------------

ttk.Label(similarity, text=u"选择acfun用户ID:").grid(column=0, row=0,padx=10,pady=5, sticky=tk.W)
number = tk.IntVar()
numberChosen = ttk.Combobox(similarity, width=20, textvariable=number,state='readonly') #3
numberChosen['values'] = '414992'
numberChosen.grid(column=1, row=0,sticky=tk.W)
numberChosen.current(0)

ttk.Button(similarity, text = u"查看用户信息",
           command = lambda : getUser(numberChosen.get())
           ).grid(column =0,row =1,padx=10,pady=5,sticky=tk.W
           )


#----------------------------方法区---------------------------
def getUser(userid):
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    a_records = ()
    b_records = ()
    b_id =''
    print(userid)
    try:
        conn.select_db("MigrationDetection01")
        cur = conn.cursor()
        #查找b_id
        sql1='SELECT b_id FROM MigrationDetection01.Mappingresult_symm where a_id = %s;'
        cur.execute(sql1,userid)
        b_id = cur.fetchone()[0]

        # 查找用户在acfun的信息
        sql = "SELECT username,signature,videocount,playnum FROM MigrationDetection01.acfun_uppers_detail where id =%s; "
        cur.execute(sql,userid)
        a_records = cur.fetchall()

        # 查找用户在bilibili的信息
        sql2 = "SELECT name,sign,videocount,playnum FROM MigrationDetection01.bilibili_uppers_detail where id =%s; "
        cur.execute(sql2, b_id)
        b_records = cur.fetchall()

    except Exception:
        print(Exception)
    finally:
        conn.close()

    # 更新页面上A站用户信息
    a_usernameVar.set(a_records[0][0])
    a_signVar.set(a_records[0][1])
    a_IDVar.set(userid)
    a_videoVar.set(a_records[0][2])
    a_playVar.set(a_records[0][3])
    # 更新页面上B站用户信息
    b_usernameVar.set(b_records[0][0])
    b_signVar.set(b_records[0][1])
    b_IDVar.set(b_id)
    b_videoVar.set(b_records[0][2])
    b_playVar.set(b_records[0][3])


#----------------------------UI区-----------------------------
ttk.Label(similarity, text=u"Acfun信息:").grid(column=0, row=2, padx=10,pady=10,sticky=tk.W)
ttk.Label(similarity, text=u"Bilibili信息:").grid(column=0, row=9,padx=10, pady=10,sticky=tk.W)
# ttk.Label(similarity, text=u"行为相似度:").grid(column=0, row=8, pady=15,sticky=tk.W)

methods=[u'用户名',u'用户签名',u'用户ID',u'用户发布视频数量',u'用户累计播放量',u'最近活跃时间']

a_usernameVar = tk.StringVar()
a_usernameVar.set('')
a_signVar = tk.StringVar()
a_signVar.set('')
a_IDVar = tk.StringVar()
a_IDVar.set('')
a_videoVar = tk.StringVar()
a_videoVar.set('')
a_playVar = tk.StringVar()
a_playVar.set('')
a_timeVar = tk.StringVar()
a_timeVar.set('2018-03-09')

b_usernameVar = tk.StringVar()
b_usernameVar.set('')
b_signVar = tk.StringVar()
b_signVar.set('')
b_IDVar = tk.StringVar()
b_IDVar.set('')
b_videoVar = tk.StringVar()
b_videoVar.set('')
b_playVar = tk.StringVar()
b_playVar.set('')
b_timeVar = tk.StringVar()
b_timeVar.set('2018-03-09')

#Acfun 展示区域
# 获取的用户名
ttk.Label(similarity, text='用户名').grid(column=0, row=3,padx=20, sticky=tk.W)
ttk.Label(similarity, textvariable=a_usernameVar).grid(column=1, row=3, sticky=tk.W)
# 获取的用户签名
ttk.Label(similarity, text=u'用户签名').grid(column=0, row=4, padx=20,sticky=tk.W)
ttk.Label(similarity, textvariable=a_signVar).grid(column=1, row=4, sticky=tk.W)
# 获取的用户ID
ttk.Label(similarity, text=u'用户ID').grid(column=0, row=5,padx=20, sticky=tk.W)
ttk.Label(similarity, textvariable=a_IDVar).grid(column=1, row=5, sticky=tk.W)
# 获取的用户视频数量
ttk.Label(similarity, text=u'用户发布视频数量').grid(column=0, row=6,padx=20, sticky=tk.W)
ttk.Label(similarity, textvariable=a_videoVar).grid(column=1, row=6, sticky=tk.W)
# 获取的用户累计播放量
ttk.Label(similarity, text=u'用户累计播放量').grid(column=0, row=7,padx=20, sticky=tk.W)
ttk.Label(similarity, textvariable=a_playVar).grid(column=1, row=7, sticky=tk.W)
# 获取的用户最近活跃时间
ttk.Label(similarity, text=u'最近活跃时间').grid(column=0, row=8,padx=20, sticky=tk.W)
ttk.Label(similarity, textvariable=a_timeVar).grid(column=1, row=8, sticky=tk.W)

# #Bilibili 展示区域
ttk.Label(similarity, text='用户名').grid(column=0, row=10, padx=20,sticky=tk.W)
ttk.Label(similarity, textvariable=b_usernameVar).grid(column=1, row=10, sticky=tk.W)
# 获取的用户签名
ttk.Label(similarity, text=u'用户签名').grid(column=0, row=11,padx=20, sticky=tk.W)
ttk.Label(similarity, textvariable=b_signVar).grid(column=1, row=11, sticky=tk.W)
# 获取的用户ID
ttk.Label(similarity, text=u'用户ID').grid(column=0, row=12,padx=20, sticky=tk.W)
ttk.Label(similarity, textvariable=b_IDVar).grid(column=1, row=12, sticky=tk.W)
# 获取的用户视频数量
ttk.Label(similarity, text=u'用户发布视频数量').grid(column=0, row=13,padx=20, sticky=tk.W)
ttk.Label(similarity, textvariable=b_videoVar).grid(column=1, row=13, sticky=tk.W)
# 获取的用户累计播放量
ttk.Label(similarity, text=u'用户累计播放量').grid(column=0, row=14, padx=20,sticky=tk.W)
ttk.Label(similarity, textvariable=b_playVar).grid(column=1, row=14, sticky=tk.W)
# 获取的用户最近活跃时间
ttk.Label(similarity, text=u'最近活跃时间').grid(column=0, row=15,padx=20, sticky=tk.W)
ttk.Label(similarity, textvariable=b_timeVar).grid(column=1, row=15, sticky=tk.W)
ttk.Label(similarity, text='').grid(column=0, row=16,padx=20, sticky=tk.W)






#----------------------------UI区-----------------------------
combVar = tk.IntVar()
combVar.set(99)


# 预测的迁移概率
ttk.Label(network, text='').grid(column=0, row=0, sticky=tk.W)
ttk.Label(network, text='').grid(column=0, row=1, sticky=tk.W)
ttk.Label(network, text='选择预测模型').grid(column=0, row=2, padx=10,sticky=tk.W)
tk.Radiobutton(network, text='MGML', variable=combVar, value=0).grid(column=0, row=3, sticky=tk.W)
tk.Radiobutton(network, text='MGBSC', variable=combVar, value=1).grid(column=0, row=4, sticky=tk.W)
tk.Radiobutton(network, text='MGLSD', variable=combVar, value=2).grid(column=0, row=5, sticky=tk.W)

ttk.Button(network, text = u"开始预测",
           command = lambda : getUser(numberChosen.get())
           ).grid(row = 6, column = 0,padx=10, pady=10,sticky=tk.E)

MigProbVar = tk.StringVar()
MigProbVar.set('0.78')
MigDirectVar = tk.StringVar()
MigDirectVar.set('Acfun->Bilibili')

ttk.Label(network, text='').grid(column=0, row=7, sticky=tk.W)
ttk.Label(network, text='').grid(column=0, row=8, sticky=tk.W)
ttk.Label(network, text="迁移概率").grid(column=0, row=9, padx=20,sticky=tk.W)
ttk.Label(network, textvariable=MigProbVar).grid(column=1, row=9, sticky=tk.W)
ttk.Label(network, text="迁移方向").grid(column=0, row=10, padx=20,sticky=tk.W)
ttk.Label(network, textvariable=MigDirectVar).grid(column=1, row=10, sticky=tk.W)
ttk.Label(network, text='').grid(column=0, row=11, sticky=tk.W)
ttk.Label(network, text='').grid(column=0, row=12, sticky=tk.W)
ttk.Label(network, text='').grid(column=0, row=13, sticky=tk.W)
ttk.Label(network, text='').grid(column=0, row=14, sticky=tk.W)
ttk.Label(network, text='').grid(column=1, row=15, sticky=tk.W)
ttk.Label(network, text='').grid(column=1, row=16, sticky=tk.W)
ttk.Label(network, text='').grid(column=1, row=17, sticky=tk.W)

# ttk.Label(network, text=u"参数设置").grid(column=0, row=0, pady=10,sticky=tk.W)
# ttk.Label(network, text=u"组合方式:").grid(column=0, row=1, pady=15,sticky=tk.W)
#
# combation=["快速Katz+Clique聚类+余弦相似度","快速Katz+Clique聚类+广义Jaccard系数","快速Katz+时空分布图卷积+余弦相似度",
#           "快速Katz+时空分布图卷积+广义Jaccard系数","随机游走+Clique聚类+余弦相似度","随机游走+Clique聚类+广义Jaccard系数",
#           "随机游走+时空分布图卷积+余弦相似度","随机游走+时空分布图卷积+广义Jaccard系数"]
#
# tk.Radiobutton(network, text=combation[0], variable=combVar, value=0).grid(column=0, row=2, sticky=tk.W)
# tk.Radiobutton(network, text=combation[1], variable=combVar, value=1).grid(column=0, row=3, sticky=tk.W)
# tk.Radiobutton(network, text=combation[2], variable=combVar, value=2).grid(column=0, row=4, sticky=tk.W)
# tk.Radiobutton(network, text=combation[3], variable=combVar, value=3).grid(column=0, row=5, sticky=tk.W)
# tk.Radiobutton(network, text=combation[4], variable=combVar, value=4).grid(column=0, row=6, sticky=tk.W)
# tk.Radiobutton(network, text=combation[5], variable=combVar, value=5).grid(column=0, row=7, sticky=tk.W)
# tk.Radiobutton(network, text=combation[6], variable=combVar, value=6).grid(column=0, row=8, sticky=tk.W)
# tk.Radiobutton(network, text=combation[7], variable=combVar, value=7).grid(column=0, row=9, sticky=tk.W)


# ttk.Label(network, text=u"保留邻居数目k:").grid(column=0, row=10, pady=20,sticky=tk.W)
# number = tk.IntVar()
# numberChosen = ttk.Combobox(network, width=10, textvariable=number,state='readonly') #3
# numberChosen['values'] = range(5,21)
# numberChosen.grid(column=0, row=10, pady=20)
# numberChosen.current(0)

# ttk.Button(network, text = u"开始构建",
           # command = unigraph).grid(row = 11, column = 0, columnspan=2, pady=20
           #                          )

#=============================================================
#程序运行
#=============================================================
win.mainloop()