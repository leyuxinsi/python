from helpers import db2

conn , cur = db2.mysql_connect()

query = "select * from qq_number"
cur.execute(query)

for item in cur.fetchall():
    sql = "update qq_number set name='南京互联网内推群(43393387)'"
    cur.execute(sql)
    conn.commit()
    print(item['number'])