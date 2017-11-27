import pymysql


class Db():
    """python数据库链接类"""

    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "yanying"
        self.password = "123456"
        self.database="bidianer"
        self.charset="utf8"

        # self.version = 'prod'
        self.version = 'dev'

    def connect(self):
        if self.version == 'prod':
            self.host = "121.40.161.194"
            self.password = "YanYing.password@allWhere;"

        db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        return [db, cursor]