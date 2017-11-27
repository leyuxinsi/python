import pymysql

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'yanying',passwd='123456',db='crawler',charset='UTF8')
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

query = "select * from br_sour_temp where sour_index=1"
cur.execute(query)
for item in cur.fetchall():
    tags = 'bootstrap,'+item['remark']
    sql = "update br_sour_temp set remark=%s where sour_id=%s"
    cur.execute(sql,(tags,item['sour_id']))
    conn.commit()



    # query = "insert into br_sour_temp(name,summary,sour_cover,sour_url,remark,sour_index,github_url) values(%s,%s,%s,%s,%s,%s,%s)"
    # if not item['official_url']:
    #     item['official_url'] = item['github_url']
    # cur.execute(query,(item['name'], item['summary'], item['cover'], item['official_url'], item['remark'], item['sour_index'],item['github_url']))
    # conn.commit()
    # sql = "update awesomes set is_update=1 where sour_id='{}'".format(item['sour_id'])
    # cur.execute(sql)
    # conn.commit()
    print(item['sour_id'])

cur.close()