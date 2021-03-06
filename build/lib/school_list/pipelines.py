# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from items import SchoolListItem
from scrapy.conf import settings
import pymongo


class SchoolListPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        school = dict(item)
        self.post.save(school)   # 这里用save意思是, 如果数据存在, 则直接update, 不存在则insert
        return item
