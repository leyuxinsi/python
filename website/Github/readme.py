from urllib import request
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'yanying',passwd='123456',db='crawler',charset='UTF8')
cur = conn.cursor()

url = "https://github.com/CraryPrimitiveMan/awesome-php-zh_CN/blob/master/README.md"

data = request.urlopen(url).read().decode('utf8')
soup = BeautifulSoup(data,'html5lib')
i=0
index = 0
article = soup.find('article')
for h2 in article.find_all('h2'):
    index += 1
    if i < 2:
        i +=1
        continue
    # 当前ul列表标题
    title = h2.get_text()
    summary = h2.find_next('p').get_text()
    print(title)
    #print(summary)
    print('---------------------')
    # 获取列表ul
    lists = h2.find_next_sibling('ul').find_all('li')
    for li in lists:
        sour_title = li.find('a').get_text()
        sour_url = li.find('a').get("href")
        li.a.clear()
        sour_summary = li.get_text()
        query = "insert into br_github(name,summary,sour_cover,sour_url,remark,sour_index) values('{}','{}','{}','{}','{}','{}')".format(sour_title,sour_summary,'',sour_url,title,index)
        cur.execute(query)
        conn.commit()
        print(sour_title,sour_url,sour_summary)

    print('=========================')

cur.close()
conn.close()