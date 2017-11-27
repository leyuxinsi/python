from pymongo import MongoClient

conn = MongoClient('localhost',27017)
db = conn.source

for item in db.col.find():
    print(item)