import scrapy
import logging


class douban_spider(scrapy.Spider):
    base_url = 'https://movie.douban.com/top250'
    start_urls = [base_url]
    name = 'douban'

    def parse(self, response):

        for item in response.xpath('//*[@id="content"]/div/div[1]/ol'):
            title = item.xpath('//div/div[2]/div[1]/a/span[1]/text()').extract()
            rating_num = item.xpath('//div/div[2]/div[2]/div/span[2]/text()').extract()
            logging.debug('title %s rating num %s' % (title, rating_num))

        next_btn = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]')
        # nextUrl = base_url +next_btn.xpath('//a/@href').extract()
        # if(nextUrl):



