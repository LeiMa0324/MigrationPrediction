import pymysql
import traceback
import csv
import numpy
import pandas

'''
二网重叠用户记录tag
'''

def getUsers():
    Users =[]
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
    try:
        conn.select_db("MigrationDetection03")
        cur = conn.cursor()
        sql = 'SELECT a_id,b_id FROM MigrationDetection03.overlap_user_two_network;'
        cur.execute(sql)
        records = cur.fetchall()
        for r in records:
            Users.append(list(r))
    except Exception:
        print(Exception)
    finally:
        conn.close()
    print('get user done')
    return Users

class User(object):

    aid =''
    bid=''
    ac_tags ={}
    bili_tags = {}


    # 初始化
    def __init__(self,aid,bid):
        self.aid = aid
        self.bid = bid
        self.ac_tags = {}
        self.bili_tags = {}
        print('初始化用户%s和%s...'%(aid,bid))
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection03")
            cur = conn.cursor()
            sql = 'SELECT tags FROM overlap_acfun_video_two_network where uid =%s;'
            cur.execute(sql,self.aid)
            records = cur.fetchall()
            # 所有视频的tag
            for video in records:
                # 单个视频的tag
                for tagsforvideo in video:
                    taglist = tagsforvideo.split(',')
                    for tag in taglist:
                        # 获取tag名
                        tagname = self.getactagname(tag)
                        # 计数+1
                        if tagname in self.ac_tags.keys():
                            self.ac_tags[tagname] +=1
                        else:
                            self.ac_tags[tagname] =1
                        # print('计数为%d'%self.ac_tags[tag])

        except Exception as err:
            print(err)
            print(traceback.print_exc())
        finally:
            conn.close()

        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection03")
            cur = conn.cursor()
            sql = 'SELECT tags FROM overlap_bili_video_two_network where mid =%s;'
            cur.execute(sql,self.bid)
            records = cur.fetchall()
            for video in records:
                for tagsforvideo in video:
                    taglist = tagsforvideo.split(',')
                    for tag in taglist:
                        tagname= self.getbilitagname(tag)
                        # 计数+1
                        if tagname in self.bili_tags.keys():
                            self.bili_tags[tagname] +=1
                        else:
                            self.bili_tags[tagname] =1
                        # print('计数为%d' % self.bili_tags[tag])
        except Exception as err:
            print(err)
            print(traceback.print_exc())
        finally:
            conn.close()

    # 获取acfuntag名
    def getactagname(self,tagid):
        tagname =''
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection03")
            cur = conn.cursor()
            sql = 'SELECT tagName FROM acfun_tag where tagId =%s;'
            cur.execute(sql, tagid)
            record = cur.fetchone()
            tagname =record[0]
        except Exception as err:
            print(err)
        finally:
            conn.close()
        return tagname

    # 获取bilitag名
    def getbilitagname(self,tagid):
        tagname =''
        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection03")
            cur = conn.cursor()
            sql = 'SELECT tagname FROM bilibili_tags where tagid =%s;'
            cur.execute(sql, tagid)
            record = cur.fetchone()
            if record:
                tagname =record[0]
        except Exception as err:
            print(err)
        finally:
            conn.close()
        return tagname

    # 获取ac_tags列表和计数
    def getactags(self):
        return self.ac_tags

    # 获取bili_tags列表和计数
    def getbilitags(self):
        return self.bili_tags


    def getids(self):
        return [self.aid,self.bid]

    def savetags(self):
        Adata =[]
        Bdata =[]
        for name in self.ac_tags.keys():
            Adata.append([self.aid,self.bid,name,self.ac_tags[name],'A'])

        for name in self.bili_tags.keys():
            Adata.append([self.aid,self.bid,name,self.bili_tags[name],'B'])

        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection03")
            cur = conn.cursor()
            sql = 'INSERT INTO `MigrationDetection03`.`tag_count`(a_id,b_id,tagname,num,abFlag)VALUES(%s,%s,%s,%s,%s);'
            cur.executemany(sql,Adata)
            conn.commit()
            print('A站tag插入完毕')
        except Exception as err:
            print(err)
        finally:
            conn.close()

        conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset="utf8")
        try:
            conn.select_db("MigrationDetection03")
            cur = conn.cursor()
            sql = 'INSERT INTO `MigrationDetection03`.`tag_count`(a_id,b_id,tagname,num,abFlag)VALUES(%s,%s,%s,%s,%s);'
            cur.executemany(sql,Bdata)
            print('B站tag插入完毕')
            conn.commit()
        except Exception as err:
            print(err)
        finally:
            conn.close()


Users = getUsers()
for u in Users:
    user = User(u[0],u[1])
    print(user.getactags())
    print(user.getbilitags())
    user.savetags()
