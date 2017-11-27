# coding=utf-8

from bs4 import BeautifulSoup
from helpers import db2
import requests

conn , cur = db2.mysql_connect()


def insert_tags(tags,icon):
    query = "insert into br_tags(tags_name,cover) values('{}','{}')".format(tags,icon)
    cur.execute(query)
    conn.commit()


def check_repeat(tags_name):
    query = "select * from br_tags where tags_name='{}'".format(tags_name)
    cur.execute(query)
    return cur.fetchone()


def update_cover(tags_id,cover):
    query = "update br_tags set cover='{}' where tags_id='{}'".format(cover, tags_id)
    cur.execute(query)
    conn.commit()


query= "select * from br_tags"
cur.execute(query)
for item in cur.fetchall():
    if item['cover']:
        if not item['cover'].startswith('2016'):
            update_cover(item['tags_id'],'201707/26/'+item['cover'])


