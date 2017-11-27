from helpers import db2

conn_loc , cur_loc = db2.local_mysql_connect()
conn , cur = db2.mysql_connect()

query = "SELECT * FROM br_source_temp"
cur_loc.execute(query)


def send_data(name,content,cover,url,tags):
    query = "insert into br_source_temp(name,content,sour_cover,sour_url,sour_tags) values(%s,%s,%s,%s,%s)"
    cur.execute(query, [name.strip(), content.strip(), cover.strip(), url.strip(), tags.strip()])
    conn.commit()

for item in cur_loc.fetchall():
    print(item['name'])
    send_data(item['name'],item['content'],item['sour_cover'],item['sour_url'],item['sour_tags'])
    print("---------")

conn_loc.close()
conn.close()