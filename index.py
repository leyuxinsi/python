import urllib
from urllib import parse
from urllib import request
from bs4 import BeautifulSoup
from pprint import pprint
import pymysql
import json

#抓取github

db = pymysql.connect(
    host="127.0.0.1",
    user="yanying",
    password="123456",
    database="bidianer",
    charset='utf8'
)
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

url = 'https://zhuanlan.zhihu.com/p/27283077'
header = {
    'Cookie':'q_c1=aeb58fa09c9e475eb1038171398a576f|1496971539000|1496971539000; r_cap_id="MWQzZjAzZWRhMTcyNDk2OGExNWEzYWI4YTFhYTBiZTM=|1497243490|1ba580ac324ffea6dd8e5ce94b6c395ea2927886"; cap_id="MGFkYmY0MmYwZDY0NDlhNDk5ZTM1MDg3Y2E3MmYxMDg=|1497243490|9c6595a99dc1224d29810fd1100a3001d1dd955c"; d_c0="ADCCdVK-5guPTvmvzBI7v_GoR9qeBitK6IY=|1497243491"; _zap=54f1f19c-e7d4-4d84-9f79-a8d1d0346f5a; _xsrf=2|a9a5228a|4dd029117bad2d51f4a178aa7b80a543|1497320561; _ga=GA1.2.576220217.1497243504; z_c0=Mi4wQUFEQTk5TVpBQUFBTUlKMVVyN21DeGNBQUFCaEFsVk5kS3hsV1FDVjNfZENJSnh2bkZHeEZZSXlOcnZpNzFraGJR|1497506399|cfdccbd853785d1fa4da804b20b02719d62fb5d8; aliyungf_tc=AQAAAJwvRUhmRQsAPX/dckGm9Xd9cFv6; XSRF-TOKEN=2|16cf9c59|f2ba97c2c4c793824bcbc679c4ea1b90|1497320561; __utma=155987696.576220217.1497243504.1498009009.1498009009.1; __utmb=155987696.0.10.1498009009; __utmc=155987696; __utmz=155987696.1498009009.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
    'Referer':'https://segmentfault.com/r/1250000009843649?shareId=1210000009843650',
    'Connection':'keep-alive',
}

request_data = request.Request(url,headers=header)

data = request.urlopen(request_data).read()
data = data.decode('UTF-8')
soup = BeautifulSoup(data,"html5lib")

content = soup.find(id="preloadedState")
content = json.loads(content.contents[0])

posts = content['database']['Post']['27283077']['content']

the_soup = BeautifulSoup(posts,'html5lib')

post_h4 = the_soup.find_all('h4')
for h4 in post_h4:

    h4_text = h4.get_text()
    #print('=====================================')
    post_ul = h4.find_next_sibling('ul')
    for li in post_ul.find_all('li'):
        href_a =  li.find('a')
        title = href_a.get_text().strip()
        tag_href = parse.unquote(href_a.get('href'))
        tag_href_copy = tag_href[(tag_href.find('?')+8):]
        li_a = li.a
        li_a.clear()
        li_text = li.get_text().replace('–','')
        li_text = li_text.strip()
        #print(title,li_text,'----',tag_href_copy)

        query = "insert into br_crawler(name,content,sour_url,remark) values('{}','{}','{}','{}')".format(title,li_text,tag_href_copy,h4_text)
        cursor.execute(query)
        db.commit()
        print(h4_text)

cursor.close()
db.close()