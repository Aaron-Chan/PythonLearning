import scrapy
import logging


class douban_spider(scrapy.Spider):
    start_urls = ['https://movie.douban.com/top250']
    name = 'douban'

    def parse(self, response):


        for item in response.xpath('//*[@id="content"]/div/div[1]/ol'):
            title = item.xpath('//div/div[2]/div[1]/a/span[1]/text()').extract()
            rating_num = item.xpath('//div/div[2]/div[2]/div/span[2]/text()').extract()
            logging.debug('title %s rating num %s' % (title, rating_num))
