import pymysql

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'yanying',passwd='123456',db='crawler',charset='UTF8')
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

query = "SELECT tags FROM br_opendigg GROUP BY tags"
cur.execute(query)
i=0
for item in cur.fetchall():
    if item['tags']:
        sql_b = "select * from br_opendigg where tags='{}'".format(item['tags'])
        cur.execute(sql_b)
        for sour in cur.fetchall():
            sql = "update br_opendigg set sour_index='{}' where sour_id='{}'".format(i,sour['sour_id'])
            cur.execute(sql)
            conn.commit()
            print(sour['sour_id'])
        print('========')
        i += 1