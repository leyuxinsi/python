from helpers import db2

conn , cur = db2.local_mysql_connect()

query = "SELECT * FROM br_source_temp"
cur.execute(query)


def save_data(sour_id , name):
    query = "update br_source_temp set name=%s where sour_id=%s"
    cur.execute(query,[name,sour_id])
    conn.commit()

for item in cur.fetchall():
    name = item['name']
    clear_name = name[name.find('.')+1:]
    print(clear_name.strip())
    save_data(item['sour_id'],clear_name)