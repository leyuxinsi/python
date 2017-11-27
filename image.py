import requests
from lxml import html

def get_name(src):
    arr = src.split('/')

    while '' in arr:
        arr.remove('')

    arr = arr[:4]
    arr.append('strip')
    url = 'http://' + '/'.join(arr)

    return [arr[2].split('?')[0] , url]

p_id = input('输入一个文章ID：')
url = 'http://www.jianshu.com/p/{}'.format(p_id)

object = requests.get(url).content
document = html.fromstring(object)

print(requests.get(url).text)

title = document.xpath('//h1[@class="title"]/text()')[0].strip()
images = document.xpath('//div[@class="show-content"]/div[@class="image-package"]/img/@src')
exit()
for item in images:
    file_path = get_name(item)
    img_obj = requests.get(file_path[1]).content
    with open('image/'+file_path[0], 'wb') as p:
        p.write(img_obj)

    print(file_path[0])


