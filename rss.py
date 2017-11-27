# -*- coding:utf-8 -*-
import feedparser
from bs4 import BeautifulSoup
from helpers.crawler import Crawler
from pprint import pprint
import datetime
import socket

socket.setdefaulttimeout(10)

crawler = Crawler()


def main(rss_id, name, rss_url):
    print(rss_id, '-', name)
    try:
        data = feedparser.parse(rss_url)

        # pprint(data.entries[0])
        # format_gmt = '%a, %d %b %Y %H:%M:%S +0000'
        # published_date = datetime.datetime.strptime(data.entries[0].published, format_gmt)
        # print(published_date)
        #
        # exit()

        for item in data.entries:
            try:
                # 检查是否重复
                if crawler.check_repeat(item['link']):
                    print('exits')
                    continue

                cover = ''
                title = item['title']
                link = item['link']

                # 如果有img这个键，那么直接使用
                if item.has_key('img'):
                    cover = item['img']

                # 如果有content字段，那么summary为简短描述，否则为文章内容
                if item.has_key('content'):
                    content = item['content'][0]['value']
                    summary = item['summary'].replace("\n", "")
                    soup = BeautifulSoup(content, 'html5lib')
                    img_obj = soup.find('img')
                    if not cover:
                        if img_obj:
                            cover = soup.find('img').get('src')
                        else:
                            cover = ''
                elif item.has_key('summary'):
                    content = item['summary']
                    soup = BeautifulSoup(content, 'html5lib')
                    img_obj = soup.find('img')
                    if not cover:
                        if img_obj:
                            cover = soup.find('img').get('src')
                        else:
                            cover = ''
                    summary = soup.get_text().replace("\n", "")[0:100]
                else:
                    summary = item['link']

                save_path = crawler.get_img(cover)

                tag_arr = []
                if item.has_key("tags"):
                    for tag_item in item['tags']:
                        tag_arr.append(tag_item['term'])

                print(title)
                print(save_path)

                crawler.insert_temp(title, summary, save_path, ",".join(tag_arr), link, rss_id, item.published)
                crawler.insert_url(link)

            except Exception as e:
                print(e)
        print('==============')
        crawler.update_rss(rss_id)
    except Exception as e:
        print(e)


if __name__ == '__main__':

    rss_lists = crawler.get_rss_lists()

    for rss_item in rss_lists:
        main(rss_item['rss_id'],rss_item['name'],rss_item['rss_url'])
