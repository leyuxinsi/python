import requests,base64
from urllib import request
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
            "Cookie": "__cfduid=dc1e3f5ec0b5daa772aeaafa723f7650d1508394323; _ga=GA1.2.1890453381.1508394171",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Host":"img.jandan.net",
    "Referer":"http://jandan.net/2017/11/05/new-quark-fusion.html",
    "Upgrade-Insecure-Requests":"1",
    "Connection":"keep-alive",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Pragma":"no-cache",
    "Cache-Control":"no-cache"

        }

url = 'http://img.jandan.net/news/2017/10/813d79a909d10cc1eeea9f794f4b2d33.jpg'
request_data = request.Request(url,headers=headers)
data = request.urlopen(request_data).read()
print(data)
print(data.decode('utf-8'))

exit()
obj = requests.get('http://img.jandan.net/news/2017/10/813d79a909d10cc1eeea9f794f4b2d33.jpg',headers=headers).content

print(base64.b64decode(obj))
with open('upload/abc.png','wb') as f:
    f.write(base64.b64decode(obj))