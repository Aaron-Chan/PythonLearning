# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymysql

class TutorialPipeline(object):
    def __init__(self):
        self.file = codecs.open('data_cn.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(bytearray(line,"unicode_escape").decode('utf-8'))
        return item

class MySqlMoviePipeline(object):
    def __init__(self):
        db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')

