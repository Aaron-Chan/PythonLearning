# -*- coding:utf-8 -*-
DOU_BAN_URL = "https://movie.douban.com/top250"
CHROME_USER_AGENT = 'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

import requests
from bs4 import BeautifulSoup
import re
# 先看下豆瓣top250的html结构
#
# 总计分析html方法
# 编码找出对应信息并打印
# 看如何用echart表示
custom_headers = {'user-agent': CHROME_USER_AGENT}


class MovieInfo:
    '''电影信息 名称 导演  主演 编剧 评分 国家'''
    def __init__(self, name, rating_num, director, staring_list, country):
        self.name = name
        self.rating_num = rating_num
        self.director = director
        self.staring_list = staring_list
        self.country = country


movies_url_list = []
movies_info_list = []


def test():
    for star_page in range(0, 250, 25):
        url = "%s?start=%s&filter=" % (DOU_BAN_URL, star_page)
        getMovieUrl(url)
    print(len(movies_url_list))
    for movie_url in movies_url_list:
        requestMovieUrl(movie_url)


def requestMovieUrl(movie_url):
    print(movie_url)
    r = requests.get(movie_url, headers=custom_headers)
    if not r.status_code == 200:
        print("response not ok")
        return False
    soup = BeautifulSoup(r.content)

    content = soup.find('div', attrs={'id': 'content'})

    title = content.find('span', attrs={'property': 'v:itemreviewed'}).getText()
    year = content.find('span', attrs={'class': 'year'}).getText()
    year= re.sub('[(|)]','',year)


    director = content.find('a', attrs={'rel': 'v:directedBy'}).getText()
    print(title)
    print(year)
    print(director)

    starings = content.find_all('a', attrs={'rel': 'v:starring'})

    rating_num = content.find('strong', attrs={'property': 'v:average'}).getText()
    print(rating_num)
    staring_list=[]
    for star in starings:
        staring_list.append(star.getText())

    country = content.find('span',attrs={'class': 'pl'},text='制片国家/地区:').next_sibling.string.strip()
    movie_info = MovieInfo(title,rating_num,director,staring_list,country)
    movies_info_list.append(movie_info)


def getMovieUrl(url):
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
        hd = detail.find('div', attrs={'class': 'hd'})
        # movie_title = hd.find('span', attrs={'class', 'title'}).getText()
        movie_url = hd.a['href']
        # rating_num = detail.find('div', attrs={'class': 'bd'}).find('span', attrs={'class', 'rating_num'}).getText()
        print(movie_url)
        if movie_url:
            movies_url_list.append(movie_url)
    return True


def test1():
    requestMovieUrl("https://movie.douban.com/subject/1292052/")


if __name__ == '__main__':
    test()
    print(len(movies_info_list))
