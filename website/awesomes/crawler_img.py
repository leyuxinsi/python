import requests,pymysql,os,uuid

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'yanying',passwd='123456',db='crawler',charset='UTF8')
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

query = "select sour_id,sour_cover from awesomes where is_update='0'"
cur.execute(query)

upload_dir = '201707/06/'
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

for item in cur.fetchall():
    file_name = str(uuid.uuid1())
    file_path = upload_dir + file_name.replace('-', '') + '.png'
    img_obj = requests.get(item['sour_cover']).content
    with open(file_path,'wb') as f:
        f.write(img_obj)
        print(file_path)
    sql = "update awesomes set is_update='1',cover='{}' where sour_id='{}'".format(file_path,item['sour_id'])
    cur.execute(sql)
    conn.commit()

cur.close()
conn.close()