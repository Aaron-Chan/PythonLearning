import scrapy
import logging
from  scrapy import Request


class douban_spider(scrapy.Spider):
    base_url = 'https://movie.douban.com/top250'
    base_movie_url = 'https://movie.douban.com'
    start_urls = [base_url]
    movie_urls = []
    name = 'douban'

    def parse(self, response):

        for item in response.xpath('//*[@id="content"]/div/div[1]/ol'):
            title = item.xpath('//div/div[2]/div[1]/a/span[1]/text()').extract()
            rating_num = item.xpath('//div/div[2]/div[2]/div/span[2]/text()').extract()
            logging.debug('title %s rating num %s' % (title, rating_num))
            url = self.base_movie_url + response.xpath('.//div/div[2]/div[1]/a/@href').extract()[0]
            self.movie_urls.append(url)

        next_btn = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]')
        logging.debug(next_btn.xpath('.//a/@href').extract())
        nextUrl = self.base_url + next_btn.xpath('.//a/@href').extract()[0]

        if (nextUrl):
            yield Request(nextUrl, callback=self.parse)
        else:
            for movie_url in self.movie_urls:
                yield Request(movie_url, callback=self.pase_movie)

    def parse(self, response):
        pass
