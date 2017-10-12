import re
import scrapy
import logging
from scrapy import Request

from ..items import MovieItem


class douban_spider(scrapy.Spider):
    base_url = 'https://movie.douban.com/top250'
    allowed_domains = ["douban.com"]
    base_movie_url = 'https://movie.douban.com'
    start_urls = [base_url]
    movie_urls = []
    name = 'douban'

    def parse(self, response):
        """解析出每部电影网址，保存到数组 并请求下一页数据"""

        for item in response.xpath('//ol[@class="grid_view"]/li'):
            title = item.xpath('.//span[@class="title"]/text()').extract()[0]
            rating_num = item.xpath('.//span[@class="rating_num"]/text()').extract()[0]
            logging.debug('title %s rating num %s' % (title, rating_num))
            url = item.xpath('.//div[@class="hd"]/a/@href').extract()[0]

            logging.debug(url)
            self.movie_urls.append(url)

        next_urls = response.xpath('//span[@class="next"]/a/@href').extract()
        if len(next_urls) > 0:
            yield Request(self.base_url + next_urls[0], callback=self.parse)
        else:
            for movie_url in self.movie_urls:
                yield Request(movie_url, callback=self.parse_movie)

    def parse_movie(self, response):

        """解析出每部电影的信息并保存"""
        try:
            item = MovieItem()
            name = response.xpath('//span[@property="v:itemreviewed"]/text()').extract()[0]
            year = response.xpath('//span[@class="year"]/text()').extract()[0]
            year = re.sub('[(|)]', '', year)
            print(name)
            print(year)
            director = response.xpath('//a[@rel="v:directedBy"]/text()').extract()[0]
            print(director)
            starings = response.xpath('//a[@rel="v:starring"]/text()').extract()
            print(starings)
            rating_num = response.xpath('//strong[@property="v:average"]/text()').extract()[0]
            print(rating_num)
            staring_list = []
            for star in starings:
                staring_list.append(star)

            country = response.xpath('//span[text()="制片国家/地区:"]/following-sibling::text()[1]').extract()[0].strip()
            item['name'] = name
            item['year'] = year
            item['director'] = director
            item['staring_list'] = staring_list
            item['rating_num'] = rating_num
            item['country'] = country
            yield item
            print(country)

        except BaseException as e:
            raise e
