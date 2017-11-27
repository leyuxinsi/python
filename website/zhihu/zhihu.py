# coding:utf-8
import requests
from lxml import html
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Cookie': 'q_c1=1a46f61b9d154714ba06a401cd563834|1496500514000|1496500514000; r_cap_id="Y2VlYTQ5Y2I4MTRlNDFkYjk3MzUxM2YxNGQzYmNhNzY=|1496500514|3d59093dd5a5188ae7c6a642884d215c876ab243"; cap_id="N2YwZWU5ZWQ3ZTU2NDIzNTkxODJmNWVkMmZjZmQ3NjQ=|1496500514|82bf3b7231d87f85c2eedce2e854907871b21898"; d_c0="ABCChRes2wuPTtfyYkK9pj19S0-gFgaAtf4=|1496500515"; _zap=0e0a1694-00e3-4449-a057-9dad300ca0c9; _xsrf=9b1ce3b40326ef190a705504428ab435; s-q=python%E5%92%8Cjava; s-i=7; sid=kbktr8go; z_c0=Mi4wQUFEQTk5TVpBQUFBRUlLRkY2emJDeGNBQUFCaEFsVk5OMVphV1FCWkNQWmVYazNOa0pRem1CMHlwM2U5R3Vfempn|1497086738|bbb4c08fab3428906f6b53ef256060f5b5fb8bd2; __utma=51854390.1613515282.1496500544.1496670197.1497085840.3; __utmb=51854390.0.10.1497085840; __utmc=51854390; __utmz=51854390.1497085840.3.3.utmcsr=hao123.com|utmccn=(referral)|utmcmd=referral|utmcct=/link/https/; __utmv=51854390.100-1|2=registration_date=20121030=1^3=entry_date=20121030=1',   # 你的cookie
    'Host': 'www.zhihu.com',
    'Connection': 'keep-alive',
}

def get_link_ist(collection_num):
    page = input('你想要多少页？:')
    result = []
    collection_title = None
    for i in range(1, int(page)+1):
        link = 'https://www.zhihu.com/collection/{}?page={}'.format(collection_num, i)
        response = requests.get(link, headers=headers).content
        sel = html.fromstring(response)
        # 创建文件夹
        if collection_title is None:
            # 收藏夹名字
            collection_title = sel.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()')[0].strip()
            if not collection_title:
                continue
            if not os.path.exists(collection_title):
                os.mkdir(collection_title)
        each = sel.xpath('//div[@class="zm-item"]//div[@class="zm-item-answer "]/link')
        for e in each:
            link = 'https://www.zhihu.com' + e.xpath('@href')[0]
            print(link)
            result.append(link)
    return [collection_title, result]


def get_pic(collection, answer_link):
    response = requests.get(answer_link, headers=headers).content
    #print(response)
    sel = html.fromstring(response)
    title = sel.xpath('//h1[@class="QuestionHeader-title"]/text()')[0].strip()
    try:
        # 匿名用户
        author = sel.xpath('//a[@class="UserLink-link"]/text()')[0].strip()
    except:
        author = u'匿名用户'
    # 新建路径
    path = collection + '/' + title + ' - ' + author
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        n = 1
        for i in sel.xpath('//div[@class="RichContent-inner"]//img/@src'):
            # 去除whitedot链接
            if 'whitedot' not in i:
                # print i
                pic = requests.get(i).content
                fname = path + '/' + str(n) + '.jpg'
                with open(fname, 'wb') as p:
                    p.write(pic)
                n += 1
        print(u'{} 已完成'.format(title))
    except :
        pass


if __name__ == '__main__':
    # https://www.zhihu.com/collection/69135664
    # 收藏夹号码就是：69135664
    collection_num = input('输入收藏夹号码：')
    r = get_link_ist(collection_num)
    collection = r[0]
    collection_list = r[1]
    for k in collection_list:
        get_pic(collection, k)
