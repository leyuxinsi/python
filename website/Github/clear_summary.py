import pymysql

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'yanying',passwd='123456',db='crawler',charset='UTF8')
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

query = "SELECT sour_id,summary FROM br_github"
cur.execute(query)
for item in cur.fetchone():
    summary = item['summary'].strip().replace('- ','')
    sql = "update br_github set summary='{}' where sour_id='{}'".format(summary,item['sour_id'])
    cur.execute(sql)
    conn.commit()
    print(item['summary'])

cur.close()
conn.close()