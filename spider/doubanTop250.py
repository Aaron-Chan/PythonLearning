# -*- coding:utf-8 -*-
DOU_BAN_URL = "https://movie.douban.com/top250"
CHROME_USER_AGENT = 'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

import requests
from bs4 import BeautifulSoup

# 先看下豆瓣top250的html结构
# 总计分析html方法
# 编码找出对应信息并打印
# 看如何用echart表示
custom_headers = {'user-agent': CHROME_USER_AGENT}


class MovieInfo:
    '''电影信息'''

    def __init__(self, name, rating_num, director):
        self.name = name
        self.rating_num = rating_num
        self.director = director


def test():
    for star_page in range(0, 250, 25):
        url = "%s?start=%s&filter=" % (DOU_BAN_URL, star_page)
        request(url)


def request(url):
    print(url)
    r = requests.get(url, headers=custom_headers)
    if not r.status_code == 200:
        print("response not ok")
        return False
    # print(r.content)
    soup = BeautifulSoup(r.content)
    # print(soup.prettify())
    movies_list = soup.find('ol', attrs={'class': 'grid_view'})

    for item in movies_list.find_all('li'):
        detail = item.find('div', attrs={'class': 'info'})
        movie_title = detail.find('div', attrs={'class': 'hd'}).find('span', attrs={'class', 'title'}).getText()
        rating_num = detail.find('div', attrs={'class': 'bd'}).find('span', attrs={'class', 'rating_num'}).getText()
        print('%s:%s' % (movie_title, rating_num))
    return True


if __name__ == '__main__':
    test()
