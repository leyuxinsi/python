import pymysql

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'yanying',passwd='123456',db='crawler',charset='UTF8')
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

query = "select * from br_crawler2"
cur.execute(query)

for item in cur.fetchall():
    query1="select * from cr_url where content='{}'".format(item['sour_url'])
    cur.execute(query1)
    if not cur.fetchone():
        sql = "insert into cr_url(`content`) values('{}')".format(item['sour_url'])
        cur.execute(sql)
        conn.commit()
        print(item['sour_id'])
        print(item['sour_url'])
    else:
        print('exits')