import requests
from urllib import request,parse

data = request.urlopen('https://www.bidianer.com/tags/item/php').read()
data = data.decode('UTF-8')

print(data)