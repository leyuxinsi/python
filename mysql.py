# -*- coding:utf-8 -*-
import pymysql
from pprint import pprint
import requests
import uuid
import datetime
import os

now = datetime.datetime.now()

db = pymysql.connect(
    host="127.0.0.1",
    user="yanying",
    password="123456",
    database="bidianer",
    charset='utf8'
)
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
i=0
while i<1:
    sql = 'select sour_id,sour_cover from br_crawler where sour_id>803 and is_cover=0 order by sour_id asc limit 100'

    cursor.execute(sql)
    result = cursor.fetchall()

    for item in result:
        try:
            data = requests.get(item['sour_cover']).content
            file_dir = now.strftime("%Y%m") + "/19"
            file_name = str(uuid.uuid1())
            file_path = file_dir + '/' + file_name.replace('-', '') + '.png'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            with open(file_path, 'wb') as f:
                f.write(data)
                print(file_path)
            query = "update br_crawler set cover='{}',is_cover='1' where sour_id='{}'".format(file_path, item['sour_id'])
            cursor.execute(query)
            db.commit()
        except:
            pass
    i += 1

cursor.close()
db.close()
