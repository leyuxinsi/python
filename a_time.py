import datetime

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
TIME = 'Thu, 19 Feb 2009 16:00:07 GMT'
r = datetime.datetime.strptime(TIME, GMT_FORMAT)
print(r)
