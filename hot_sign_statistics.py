#coding=utf8
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymysql



conn = pymysql.connect(host="127.0.0.1", user="root", passwd="root", charset="utf8")


sql = "SELECT * FROM bilibili.acfun_hot_signs order by c asc;"
df = pd.read_sql(sql=sql,con=conn)

'''
计算sign的累计分布图
'''
df.plot.pie(y='c',color='#008B8B',label="bili")
plt.show()