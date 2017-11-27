# coding=utf-8

from bs4 import BeautifulSoup
from helpers import db2

conn , cur = db2.mysql_connect()

file = open(r'data.html','rb')
data = file.read()

soup = BeautifulSoup(data,'html5lib')
lists = soup.find_all(class_='td-card')


def insert_number(number,name,ids):
    query = "insert into qq_number(number,name,indexs) values('{}','{}','{}')".format(number, name,ids)
    cur.execute(query)
    conn.commit()

for item in lists:
    number = item.find_next_sibling().get_text().strip()

    sql = "select * from qq_number where `number`='{}'".format(number)
    cur.execute(sql)
    if not cur.fetchone():
        insert_number(number,'南京php(496341851)','3')
        print(number)
    else:
        print('exists--'+number)