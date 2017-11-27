import pymysql
import time

# 往br_source表中插入数据

db = pymysql.connect(
    host="121.40.161.194",
    user="yanying",
    password="YanYing.password@allWhere;",
    database="bidianer",
    charset='utf8'
)
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

query = "select * from br_crawler2 c where is_cover=1 and is_submit=0 limit 500"
cursor.execute(query)
for item in cursor.fetchall():
    sour_url = item['official_url']
    github_url = item['github_url']
    if not sour_url:
        sour_url = item['github_url']
        github_url = 0
    sql = "INSERT INTO `bidianer`.`br_source` (`sour_id`, `name`, `content`, `sour_cover`, `screenshots`, `sour_url`,`github_url`, `user_id`, `useful_amount`, `collect_amount`, `click_amount`, `quick_sort`, `sour_tags`, `create_time`, `update_time`, `delete_flag`, `icon_file`, `web_type`, `web_id`, `display_type`, `is_quniu`) " \
          "VALUES (NULL, '{}', '{}', '{}', '0', '{}','{}', '19', '0', '0', '0', '0.0000000000000000', '{}', '{}', {}, '0', NULL, '1', NULL, '2', '0')".format(item['name'],item['summary'],item['github_sour_cover'],sour_url,github_url,item['remark'],int(time.time()),int(time.time()))
    cursor.execute(sql)
    db.commit()

    query1 = "update br_crawler2 set is_submit='1' where sour_id='{}'".format(item['sour_id'])
    cursor.execute(query1)
    db.commit()
    print(item['sour_id'])

cursor.close()
db.close()