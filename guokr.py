from urllib import request,parse
import json
from pprint import pprint
from helpers import date
from helpers import db2
from helpers import file_dir
import os,stat
import requests

conn,cursor = db2.mysql_connect()


def checkIsRepeat(sour_url):
    query = "select * from br_url where content='{}'".format(sour_url)
    cursor.execute(query)
    result = cursor.fetchone()
    return result


def insertToUrl(sour_url):
    query = "insert into br_url(content) values('{}')".format(sour_url)
    cursor.execute(query)
    conn.commit()


def insert_data(title, summary, save_path, tags, link, rss_id):
    query = "insert into br_source_temp(name,content,sour_cover,sour_tags,sour_url,is_crawler,rss_id) values (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,(title, summary, save_path, tags, link, 1,rss_id))
    conn.commit()


def updateRss(rss_id):
    query = "update br_rss set update_time='{}' where rss_id={}".format(format_year+"-"+format_month+"-"+format_day,rss_id)
    cursor.execute(query)
    conn.commit()

format_year = date.get_year()
format_month = date.get_month()
format_day = date.get_day()
timestamp = date.get_timestamp()

upload_dir = 'upload/'+file_dir.get_upload_dir()

if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)
    os.chmod(upload_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

headers = {
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    "Cookie":'__utmt=1; __utma=253067679.469750544.1508935786.1508935786.1508935786.1; __utmb=253067679.5.9.1508935796098; __utmc=253067679; __utmz=253067679.1508935786.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=253067679.|1=Is%20Registered=No=1',
    "Connection":'keep-alive',
    "Host":"www.guokr.com",
    "Referer":"http://www.guokr.com/scientific/"
}


def crawler(offset,rss_id):
    url = 'http://www.guokr.com/apis/minisite/article.json?retrieve_type=by_subject&limit=20&offset={}&_=1508935807611'.format(offset)

    request_data = request.Request(url, headers=headers)
    data = request.urlopen(request_data).read()
    data = json.loads(data.decode('utf-8'))

    for item in data['result']:
        try:
            if checkIsRepeat(item['url']):
                print('exists')
                continue

            title = item['title']
            summary = item['summary']
            cover = item['small_image']
            link = item['url']
            tags = item['subject']['name']

            file_path = ''
            save_path = ''

            if cover:
                file_path_arr = file_dir.get_file_path(cover)
                file_path = file_path_arr[0]

                save_path = file_path_arr[1]

                img_data = requests.get(cover).content
                with open(file_path, 'wb') as f:
                    f.write(img_data)

            print(title)
            print(save_path)

            insert_data(title, summary, save_path, tags, link,rss_id)

            # 插入一份到url表
            insertToUrl(link)

            updateRss(rss_id)

        except Exception as e:
            print(e)

        print("====================")

if __name__ == '__main__':
    start_page = int(input("输入开始爬取页码？"))
    end_page = int(input('输入结束爬取页码？'))
    page_size = 20

    for item in range(start_page,end_page+1):
        print('正在爬取第'+str(item)+"页")
        offset = (item-1)*page_size
        crawler(offset,rss_id=71)