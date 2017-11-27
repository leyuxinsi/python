from bs4 import BeautifulSoup
from helpers.crawler import Crawler

crawler = Crawler()


def main(url):

    data = crawler.get_content(url)
    soup = BeautifulSoup(data, "html5lib")

    for item in soup.find_all('li'):

        title_info = item.find('h3').find('a')
        name = title_info.get_text()
        sour_url = title_info.get('href')
        cover = item.find(class_='img-box').find('img').get('src')
        summary = item.find(class_='txt-info').get_text()

        author_info = item.find(class_='account')
        author = author_info.get_text()
        head_img = author_info.get('data-headimage')
        author_url = author_info.get('href')

        # 检查是否重复
        if crawler.check_repeat(sour_url):
            print('exits')
            print("=================")
            continue

        save_path = crawler.get_img(cover)

        # 检测rss是否有了
        rss_id = crawler.check_rss_repeat(author)
        if not rss_id:
            rss_cover = crawler.get_img(head_img)
            rss_id = crawler.insert_rss(author, author_url, rss_cover)

        crawler.insert_temp(name, summary, save_path, '',sour_url, rss_id)

        crawler.insert_url(sour_url)

        print(name)
        print(save_path)
        print('=============================')

if __name__ == '__main__':

    end_page = 2

    for item in range(1, end_page):

        if item == 1:
            url = 'http://weixin.sogou.com/pcindex/pc/pc_2/pc_2.html'
        else:
            url = 'http://weixin.sogou.com/pcindex/pc/pc_2/{}.html'.format(item-1)

        print(item)
        main(url)
