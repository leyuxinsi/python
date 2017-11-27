#!/usr/bin/env Python
# coding=utf-8

import requests
from urllib import request
from bs4 import BeautifulSoup
from html import parser
import json
import pymysql

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'yanying',passwd='123456',db='crawler',charset='UTF8')
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

type = 'jQuery'

url = 'https://www.awesomes.cn/subject/{}'.format(type)

header = {
    'Host': 'www.awesomes.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': 'Hm_lvt_4eb521ea7e1a8b34ca104f2703625e64=1499258867,1499259176,1499259230,1499259249; Hm_lpvt_4eb521ea7e1a8b34ca104f2703625e64=1499261418'
}

request_data = request.Request(url, headers=header)
data = request.urlopen(request_data).read().decode('utf-8')
soup = BeautifulSoup(data,'html.parser')
script = soup.find_all('script')
json_string = script[0].get_text()[16:]
json_data = json.loads(json_string)

item_data = json_data['data'][0]['sub']['repos']
for item in item_data:
    #print(item['rootyp'])
    for module in item['typcds']:
        #print(module['typcd'])
        for sour in module['repos']:
            tags = type+','+item['rootyp']+','+module['typcd']
            title = sour['name']
            summary = sour['description_cn']
            cover = sour['cover']
            sour_url = sour['owner']+'/'+sour['alia']
            print(title,summary,cover,tags)
            query = "insert into awesomes(name,summary,sour_cover,sour_url,remark,sour_index) values(%s,%s,%s,%s,%s,%s)"
            cur.execute(query,(title, summary, cover, sour_url, tags, 3))
            conn.commit()
    print('===================')


cur.close()
conn.close()