import pymysql

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'yanying',passwd='123456',db='crawler',charset='UTF8')
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

img_host = 'https://www.awesomes.cn/repo/'

query = "select sour_id,sour_url from awesomes where is_update='0'"
cur.execute(query)
for item in cur.fetchall():
    sql = "update awesomes set sour_url='{}',is_update='1' where sour_id='{}'".format(img_host+item['sour_url'],item['sour_id'])
    cur.execute(sql)
    conn.commit()
    print(item['sour_id'])

cur.close()
