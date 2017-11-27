# coding:utf-8

from urllib import request
from urllib import parse
import json
import re
from pprint import pprint
from helpers import db2


conn , cur = db2.local_mysql_connect()

header = {
    "Cookie":r'q_c1=f30d178c896b417eb36d85934c90e7b4|1507392104000|1507392104000; r_cap_id="YmU2OGRhNjgzNjdjNDRlYThiN2VhYzhlOGVlYTY5MWI=|1507392104|f530039cab6ef62f9fed8a4b0dec4d9208bf5a3c"; cap_id="ZmU2NmIzZDZhZTQ4NGRjNWI1NjcwZWY2ZWQxYmJlMzc=|1507392104|98415ed6d889752d1f82f98f9df7448225697d4c"; l_cap_id="ZTM3YThiZDExMDBlNGQ3ZmJiZDZlOThjZTkyMDE2MTg=|1507392104|8fa62f059cc67f3e8126b43de71d18decd09214c"; d_c0="AIBCrjX4fQyPTqYs3clZ5Y57Wwom5mxV9n8=|1507392104"; _zap=916b9b27-6c5f-4007-a8e0-0e7bf8f5f06a; z_c0="2|1:0|10:1507392126|4:z_c0|92:Mi4xSDBRR0FBQUFBQUFBZ0VLdU5maDlEQ2NBQUFDRUFsVk5mb2NBV2dCdHpSSXdwWFVCQW9KdmxLd3I2Qm9XUkFsNC1R|7e9017da7299de13da85995973cd998477ee190ce62b69853406c51b05b0ceb1"; _ga=GA1.2.1656177437.1507392176; aliyungf_tc=AQAAALX3TWlNrA0AtctBMWifwoFwIW/9; s-q=%E7%88%AC%E5%8F%96%E7%9F%A5%E4%B9%8E; s-i=22; sid=lpkkgbrg; _xsrf=83335760-165c-4667-85fa-e5aaa2d2363d; __utma=51854390.1656177437.1507392176.1508836060.1508898418.17; __utmb=51854390.0.10.1508898418; __utmc=51854390; __utmz=51854390.1508898418.17.16.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20121030=1^3=entry_date=20121030=1',
    "User-Agent":r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    'Host': r'www.zhihu.com',
    'Connection': r'keep-alive',
    'Referer':'https://www.zhihu.com/topics',
    'Origin':'https://www.zhihu.com',
    'X-Requested-With':'XMLHttpRequest',
    'X-Xsrftoken':'83335760-165c-4667-85fa-e5aaa2d2363d'
}

link = r'https://www.zhihu.com/node/TopicsPlazzaListV2'


def save_data(topic_id,name,parent_id):
    query = "insert into br_zhihu_topic(zhihu_topic_id,name,parent_id,is_crawler) values(%s,%s,%s,1)"
    cur.execute(query,[topic_id,name,parent_id])
    conn.commit()


def check_repeat(topic_id):
    query = "select * from br_zhihu_topic where zhihu_topic_id=%s"
    cur.execute(query,[topic_id])
    return cur.fetchone()


def update_status(zhihu_topic_id):
    print(zhihu_topic_id)
    """更新已经抓取完的记录的状态"""
    query = "update br_zhihu_topic set is_crawler = 1 where topic_id=%s"
    cur.execute(query,[zhihu_topic_id])
    conn.commit()


def crawler(topic_id , offset,this_id):

    param = {
        'method': 'next',
        'params': '{"topic_id":'+str(topic_id)+',"offset":'+str(offset)+',"hash_id":"55824e4e9639c9441adde940f4c440db"}'
    }

    param_data = parse.urlencode(param).encode('utf-8')
    request_data = request.Request(link, headers=header, data=param_data)
    data = request.urlopen(request_data).read()
    data = data.decode('UTF-8')

    topics = json.loads(data)['msg']
    if not topics:
        update_status(this_id)
        print('====================')
        print('finish~')
        return None

    item = []
    for topic in topics:
        match = re.search(r'/topic/(\d+)', topic)
        match2 = re.search(r'<strong>(.*)</strong>', topic)
        if match and match2:
            zhihu_topic_id = match.group(1)
            topic_name = match2.group(1)
            if not check_repeat(zhihu_topic_id):
                save_data(zhihu_topic_id,topic_name,topic_id)
                print(topic_name +" - "+ zhihu_topic_id)
            else:
                print('exits - '+topic_name)

            print('===========================')

    update_status(this_id)
    return True


def get_topic_id():
    query = "select * from br_zhihu_topic where is_crawler=0 and parent_id=0 limit 5"
    cur.execute(query)
    return cur.fetchall()


if __name__ == '__main__':
    total_page = 50
    page_size = 20

    zhihu_topic = get_topic_id()

    pprint(zhihu_topic)

    for value in zhihu_topic:
        print(value['topic_id'],value['name'])
        print('+++++++++++++++++++++++++')

        inner_for = True
        for page in range(1, total_page + 1):
            print('正在爬取：第',page,'页')
            if not inner_for:
                continue

            offset = (page - 1) * page_size
            inner_for = crawler(value['zhihu_topic_id'], offset, value['topic_id'])
