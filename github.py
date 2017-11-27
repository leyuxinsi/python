# coding=utf-8

import requests
url = 'https://api.github.com/search/repositories?q=language:python&sort=starts'
r = requests.get(url)
print('status code:',r.status_code)

response_dict = r.json()

item = response_dict['items']
print(item[0])