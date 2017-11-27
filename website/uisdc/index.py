# coding=utf-8

import requests
import urllib
from urllib import request,parse
from bs4 import BeautifulSoup
import os
from helpers import file_dir,db2

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3159.5 Safari/537.36",
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


def crawler_item(url,tags):
    """
    爬取优设的文章列表
    :param url: 文章链接
    :return: void
    """
    request_data = request.Request(url, headers=headers)
    data = request.urlopen(request_data).read()
    data = data.decode('UTF-8')
    soup = BeautifulSoup(data, "html5lib")
    article = soup.find_all('h4')
    for item in article:

        # 文章标题
        name = item.find('a').get_text().strip()

        # 文章URL
        sour_url = item.find('a').get('href')
        sour_url = parse.unquote(sour_url)

        if check_repeat(sour_url):
            print('exists')
            print('-----------')
            continue

        # 爬取图片
        img_attr = item.find_next_sibling().find('img')
        if img_attr:
            img = img_attr.get('src')
            cover = crawler_img(img)
        else:
            cover = ''

        # 获取文章简介
        content = item.find_next_sibling().find_next_sibling().get_text().strip()

        # 保存数据到数据库
        save_data(name,content,cover,sour_url,tags)

        print(name)
        print(content)
        print(cover)
        print(sour_url)
        print('--------')


if __name__ == "__main__":
    crawler_item("http://www.uisdc.com/75-web-animation-tools-2",'前端开发,css3动效,js插件')