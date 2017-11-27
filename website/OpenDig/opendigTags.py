# !/usr/bin/env python
# -*- coding:utf-8 -*-
# 抓取opendigg网站的tags
import pymysql
from urllib import request
from bs4 import BeautifulSoup
import time

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'yanying',passwd='123456',db='crawler',charset='UTF8')
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

header = {
    'Cookie':'UM_distinctid=15cca67f9b12a6-098bf0254ccf5b-8373f6a-1fa400-15cca67f9b2636; _opendigg_session=ejQ0Mm5lcnU5bnhEbDgwZ2dUdk43NE52cTIwWlNYMW1kUUZyLzFRdVpuMWREQnRoaCtTak51WVZRU2tGN2pRbmI3Y1had1puYytKK1JmMVBZV2o2OHBENEZkeVk1dkJjVVpXanBtZXdYc3FDTGo2TWE3eDZybUdhQk9ndEEzZlFMYURLQWhIN3ZhZ0FCWW5ZV0NUWWdRPT0tLUFSaEJTVjVURjJjaFpETVVuY05FSmc9PQ%3D%3D--8688d1a74790ff20778cbdb5fc2350ec3a4a6b39; CNZZDATA1260869832=2069363338-1498041906-https%253A%252F%252Fwww.baidu.com%252F%7C1498047315',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Connection':'keep-alive'
}

query = "SELECT sour_id,sour_url FROM br_opendigg where tags is null limit 500"
cur.execute(query)
lists = cur.fetchall()

if lists.__len__() <= 0:
    cur.close()
    conn.close()
    exit()

for item in lists:

    request_data = request.Request(item['sour_url'], headers=header)
    try:
        data = request.urlopen(request_data).read().decode('utf-8')
        soup = BeautifulSoup(data, 'html5lib')
        all_li = soup.find(class_='breadcrumb').find_all('a')

        arr = []
        for li_item in all_li:
            arr.append(li_item.get_text())
        tags = ','.join(arr)
        print(tags)
        query = "update br_opendigg set tags='{}' where sour_id='{}'".format(tags, item['sour_id'])
        cur.execute(query)
        conn.commit()
        print(item['sour_id'],'====================')
    except (Exception)as e:
        print(e)

    time.sleep(2)


cur.close()
conn.close()

