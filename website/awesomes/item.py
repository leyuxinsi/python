#!/usr/bin/env Python
# coding=utf-8

from urllib import request
from bs4 import BeautifulSoup
from html import parser
import json
import pymysql

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'yanying',passwd='123456',db='crawler',charset='UTF8')
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

url = 'https://www.awesomes.cn/repo/angular/angular-js'

header = {
    'Host': 'www.awesomes.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': 'Hm_lvt_4eb521ea7e1a8b34ca104f2703625e64=1499258867,1499259176,1499259230,1499259249; Hm_lpvt_4eb521ea7e1a8b34ca104f2703625e64=1499261418'
}

query = "select sour_id,sour_url from awesomes where is_update=0 limit 50"
cur.execute(query)

for record in cur.fetchall():
    request_data = request.Request(record['sour_url'], headers=header)
    data = request.urlopen(request_data).read().decode('utf-8')
    soup = BeautifulSoup(data,'html.parser')
    official_url = soup.find(class_='home').get('href')
    github_url = soup.find(class_='github').get('href')

    sql = "update awesomes set official_url='{}',github_url='{}',is_update='1' where sour_id='{}'".format(official_url,github_url,record['sour_id'])
    cur.execute(sql)
    conn.commit()

    print(record['sour_id'])
    print(official_url)
    print(github_url)

    print('======================')

cur.close()
conn.close()