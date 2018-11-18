import requests
import json
import random
import pymysql
import time
from requests.exceptions import ProxyError

# def datetime_to_timestamp_in_milliseconds(d):
#     current_milli_time = lambda: int(round(time.time() * 1000))
#     return current_milli_time()
#
# print(datetime_to_timestamp_in_milliseconds())


#载入userAgent
def LoadUserAgents(uafile):

    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    return uas

uas = LoadUserAgents("user_agents.txt")
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/45388',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',

}

#获取数据函数
def getsource(mid):
    # #线程睡眠(30-60)的随机秒数
    # time.sleep(random.choice(range(1,5)))
    try:
        payload = {
            'csrf': '28a1f99320ba6aa63a5753b70b815bc7',
            'mid': mid
        }
        #随机选择useragent
        ua = random.choice(uas)
        head = {'User-Agent':ua,
            'Referer':'http://space.bilibili.com/'+str(random.randint(9000,10000))+'/',
            'Host': 'space.bilibili.com',
            'Connection': 'keep-alive',
            'Content-Length': '28',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'http://space.bilibili.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }

        s=requests.session()
        s.keep_alive = False
        response= s.post('https://space.bilibili.com/ajax/member/GetInfo', headers=head,  data=payload,
                         )
        jscontent =response.text


        # print responseCode
        if response.status_code ==200:
            print("请求成功，获取用户信息...mid:%s "%(payload["mid"]))

            #处理json数据
            print(jscontent)
            processjson(jscontent)



        else:
            print("请求失败，用户mid %s 错误码：%s "% (payload["mid"],response.status_code,))

            # #将错误id存入数据库
            # user2file(payload["mid"],response.status_code)
            # if response.status_code==429:
            #     time.sleep(100)
    except ProxyError:
        print("代理异常:")
        time.sleep(random.choice(range(60,100)))


    #打印当前时间
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

#处理json数据
def processjson(jscontent):

    # try:
    jsDict = json.loads(jscontent)
    statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
    if statusJson == True:
        if 'data' in jsDict.keys():
            jsData = jsDict['data']
            mid = jsData['mid']
            name = jsData['name']
            sex = jsData['sex']
            face = jsData['face']
            coins = jsData['coins']
            regtime = jsData['regtime'] if 'regtime' in jsData.keys() else 0
            spacesta = jsData['spacesta']
            birthday = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
            # place = jsData['place'] if 'place' in jsData.keys() else 'noplace'
            # description = jsData['description']
            # article = jsData['article']
            # fans = jsData['fans']
            # friend = jsData['friend']
            # attention = jsData['attention']
            sign = jsData['sign']
            # attentions = jsData['attentions']
            level = jsData['level_info']['current_level']
            # exp = jsData['level_info']['current_exp']
            #增加播放数
            # playnum = jsData['playNum'] if 'playNum' in jsData.keys() else 0


            regtime_format = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(regtime))
            #将要存入的数据设置为列表
            userlist=[ mid, name, sex, face, coins, regtime_format, spacesta, birthday,sign, level]
            #插入用户数据
            print('process sucessful!')
            print(userlist)
            insertuser(userlist)
        else:
            print('no data now')

    else:
        print("该用户没有json数据 ")
    # except ValueError:
    #     print('decoding json has failed')
    #     print(jscontent)


#插入用户数据到mysql数据库
def insertuser(userlist):
    conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset='utf8')
    # try:
    cur = conn.cursor()
    conn.select_db("MigrationDetection01")
    #检查是否该用户已存在
    print(userlist[0])
    # sql ='select count(*) from bili_user_addup where mid=%s;'
    # cur.execute(sql,userlist[0])
    # record=cur.fetchone()[0]
    # if record==1:
    #     print("用户在数据库中已存在！mid:%s" % userlist[0])
    # else:
    sql = 'INSERT INTO bili_user_addup VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");'%(userlist[0],userlist[1],userlist[2],userlist[3],
                                                                                 userlist[4],userlist[5],userlist[6],userlist[7],
                                                                                 userlist[8],userlist[9])
    print(sql)
    cur.execute(sql)
    print("用户成功存入数据库，mid：%d", userlist[0])
    conn.commit()
    # except Exception:
    #     print (Exception)
        #关闭数据库
    # finally:
    conn.close()

# 主程序
conn = pymysql.connect(host="223.3.76.172", user="root", passwd="123", charset='utf8',db='MigrationDetection01')
sql = 'SELECT mid FROM MigrationDetection01.bilibili_video as b where b.id is null group by mid;'
cur = conn.cursor()
cur.execute(sql)
record = cur.fetchall()
for r in record:
    getsource(r)