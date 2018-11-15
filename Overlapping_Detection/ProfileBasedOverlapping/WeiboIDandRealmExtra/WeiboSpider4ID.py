# coding=utf-8

import requests
import json
import random

url = "https://weibo.com/shushenyu?is_hot=1"

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

    'Host': 'weibo.com',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

}

ua = random.choice(uas)
head["User-Agent"] = ua
response = requests.get(url, headers=head)
print(response.text)