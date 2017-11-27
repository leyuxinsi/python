from helpers.db2 import Db
import uuid
import os
import stat
import datetime
import time
import requests
from urllib import request
import re


class Crawler():
    """python爬虫基础类"""

    def __init__(self):
        self.upload_root = 'upload/'
        self.extension = '.jpg'
        database = Db()
        #print(database.connect())
        self.conn, self.cur = database.connect()

    def create_dir(self):
        """创建图片上传目录"""

        upload_dir = self.upload_root + self.date_dir()
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            os.chmod(upload_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    def get_upload_path(self):
        """获取上传文件的完整路径"""

        file_name = str(uuid.uuid1())
        file_name = file_name.replace('-', '')+self.extension
        save_path = self.date_dir() + file_name
        return {
            "file_path": self.upload_root + save_path,
            "save_path": save_path
        }

    def date_dir(self):
        """获取日期路径"""
        return self.get_year() + "" + self.get_month() + "/" + self.get_day() + "/"

    @staticmethod
    def get_filename():
        """获取一个不重复的文件名"""
        uuid_str = str(uuid.uuid1())
        return uuid_str.replace('-', '') + '.png'

    @staticmethod
    def get_timestamp():
        """获取当前时间戳"""
        return int(time.time())

    @staticmethod
    def current_datetime():
        """获取当前datetime"""
        return datetime.datetime.now()

    def get_year(self):
        """获取当前年的数字"""
        current_time = self.current_datetime()
        return current_time.strftime('%Y')

    def get_month(self):
        """获取当前月的数字"""
        current_time = self.current_datetime()
        return current_time.strftime('%m')

    def get_day(self):
        """获取当前天的数字"""
        current_time = self.current_datetime()
        return current_time.strftime('%d')

    def get_img(self,src):
        """爬取远程的图片到本地"""
        if not src:
            return ''

        self.create_dir()
        file_path_arr = self.get_upload_path()
        file_path = file_path_arr['file_path']
        save_path = file_path_arr['save_path']

        if src[:2] == '//':
            src = 'http:' + src

        # 设计达人的图片抓取需要额外的header
        headers = {}
        if src.split('/')[2] == 'images.shejidaren.com':
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
                "Referer": "http://www.shejidaren.com/botui.html"
            }

        img_data = requests.get(src,headers=headers,timeout=10).content
        with open(file_path, 'wb') as f:
            f.write(img_data)
        return save_path

    @staticmethod
    def get_content(url,headers=''):
        """爬取远程网页内容"""
        if headers:
            request_data = request.Request(url, headers=headers)
        else:
            request_data = request.Request(url)

        data = request.urlopen(request_data).read()
        return data.decode('UTF-8')

    def check_repeat(self,sour_url):
        """检测当前资源是否已经爬取过"""
        query = "select * from br_url where content=%s"
        self.cur.execute(query, [sour_url])
        result = self.cur.fetchone()
        return result

    def insert_url(self, sour_url):
        """将爬取过的资源插入到URL管理器"""
        query = "insert into br_url(content) values(%s)"
        self.cur.execute(query, [sour_url])
        self.conn.commit()

    def insert_temp(self, title, summary, save_path, tags, link, rss_id, published):
        """将数据插入资源临时表"""
        is_crawler = 1
        if not save_path:
            is_crawler = 0

        query = "insert into br_source_temp(name,content,sour_cover,sour_tags,sour_url,is_crawler,rss_id,published)" \
                " values (%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cur.execute(query, (title, summary, save_path, tags, link, is_crawler, rss_id, self.convert_published(published)))
        self.conn.commit()

    def update_rss(self, rss_id):
        """更新RSS表的信息"""
        query = "update br_rss set update_time=%s where rss_id=%s"
        update_time = self.get_year() + "-" + self.get_month() + "-" + self.get_day()
        self.cur.execute(query, [update_time,rss_id])
        self.conn.commit()

    def insert_rss(self, name, rss_url, cover):
        """如果有新添加的rss，则直接插入到数据"""
        query = "insert into br_rss(name,rss_url,update_time,rss_icon,is_rss) values (%s,%s,%s,%s,%s)"
        update_time = self.get_year() + "-" + self.get_month() + "-" + self.get_day()
        self.cur.execute(query, (name, rss_url, update_time, cover, 0))
        last_insert_id = int(self.conn.insert_id())
        self.conn.commit()
        return last_insert_id

    def check_rss_repeat(self,rss_name):
        """检测当前RSS是否已经存在"""
        query = "select * from br_rss where name=%s"
        self.cur.execute(query, [rss_name])
        result = self.cur.fetchone()
        if result:
            return result['rss_id']
        return None

    def get_rss_lists(self):
        """获取需要爬取的Rss列表"""
        query = "SELECT * FROM br_rss where is_rss=1"
        self.cur.execute(query)
        return self.cur.fetchall()

    @staticmethod
    def convert_published(published):
        pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

        published_date = ''
        format_gmt = ''
        if published.endswith('0000'):
            format_gmt = '%a, %d %b %Y %H:%M:%S +0000'
        elif published.endswith('0800'):
            if pattern.match(published):
                published_date = published[:19]
            else:
                format_gmt = '%a, %d %b %Y %H:%M:%S +0800'
        elif published.endswith('GMT'):
            format_gmt = '%a, %d %b %Y %H:%M:%S GMT'
        elif pattern.match(published):
            published_date = published[:19]
        else:
            format_gmt = '%b %d %Y %H:%M:%S'

        if not published_date:
            published_date = datetime.datetime.strptime(published, format_gmt)

        return published_date
