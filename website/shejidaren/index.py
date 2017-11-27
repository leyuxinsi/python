# coding=utf-8

import requests
import urllib
from urllib import request,parse
from bs4 import BeautifulSoup
import os
from helpers import file_dir,db2

headers = {
    "User-Agent":"http://images.shejidaren.com/wp-content/uploads/2017/07/084229Jp7.jpg",
    "Referer":"http://www.shejidaren.com/botui.html"
}

conn , cur = db2.local_mysql_connect()


def crawler_img(src):
    upload_dir = file_dir.get_upload_dir()

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_name = file_dir.get_file_name()
    data  = requests.get(src,headers=headers).content
    with open(upload_dir+file_name,'wb') as f:
        f.write(data)

    return upload_dir+file_name


def save_data(name,content,cover,url,tags):
    query = "insert into br_source_temp(name,content,sour_cover,sour_url,sour_tags) values(%s,%s,%s,%s,%s)"
    cur.execute(query,[name,content,cover,url,tags])
    conn.commit()


def check_repeat(sour_url):
    query = "select * from br_source_temp where sour_url=%s"
    cur.execute(query,[sour_url])
    return cur.fetchone()


def crawler_lists(tags,page):
    """
    爬取设计达人标签下的文章列表
    :param tags: 文章的标签
    :param page: 文章的页码
    :return: void
    """
    url = "http://www.shejidaren.com/tag/{}/page/{}".format(parse.quote(tags),page)
    request_data = request.Request(url, headers=headers)
    data = request.urlopen(request_data).read()
    data = data.decode('UTF-8')
    soup = BeautifulSoup(data, "html5lib")
    article = soup.find_all(class_="post")
    for item in article:
        # 文章标题
        name = item.find('h2').get_text().strip()

        # 文章URL
        sour_url = item.find('h2').find('a').get('href')
        sour_url = parse.unquote(sour_url)

        if check_repeat(sour_url):
            print('exists')
            print('-----------')
            continue

        # 爬取图片
        img_attr = item.find(class_="wp-post-image")
        if img_attr:
            img = img_attr.get('src')
            cover = crawler_img(img)
        else:
            cover = ''

        # 获取文章简介
        read_more = item.find(class_='read-more')
        read_more.clear()
        content = item.p.get_text().strip()

        # 保存数据到数据库
        save_data(name,content,cover,sour_url,tags)

        print(name)
        print(content)
        print(cover)
        print(sour_url)
        print(tags)
        print('--------')


if __name__ == "__main__":
    tags = ['扁平化设计','排版','插画','摄影','海报设计','界面设计','笔刷','素材包','纹理','网站模板','网页素材','英文字体','菜单','设计趋势','配色yiqi']

    for tag in tags:
        print(tag)
        try:
            for i in range(1, 500):
                crawler_lists(tag, i)
        except (urllib.error.HTTPError) as e:
            print('没有内容啦')
            continue
        except (requests.exceptions.ConnectionError) as e:
            continue