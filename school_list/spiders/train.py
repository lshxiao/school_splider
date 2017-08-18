# -*- coding: utf-8 -*-
import hashlib
import json
import scrapy
from scrapy.http import Request


from pymongo import MongoClient
uri_1 = 'mongodb://localhost:27017/school?readPreference=nearest'
print uri_1
client1 = MongoClient(uri_1)
db1 = client1['schools']


class TrainSpider(scrapy.Spider):
    name = "train"
    allowed_domains = ["map.baidu.com"]
    start_urls = []
    map_code = db1['map_code']
    for m in map_code.find({}):
        print m.get('code')
        start_urls.append(u'http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=con&from=webmap&c=%s&wd=职业学校&wd2=&db=0&sug=0&addr=0&&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=9&tn=B_NORMAL_MAP&u_loc=12953656,4845738&ie=utf-8&pn=0&nn=0' % m.get('code'))

    def parse(self, response):
        body = json.loads(response.body)
        print '====================='
        content = body.get('content')
        rs = body.get('result')
        if content:
            for c in content:
                # print c
                name = c.get('name')
                addr = c.get('addr')
                tel = c.get('tel')
                area = c.get('area_name')
                query = rs.get('return_query')

                m = hashlib.md5()
                m.update(name.encode('utf-8'))
                item = {'_id': m.hexdigest(), 'name': name, 'tel': tel, 'addr': addr, 'area': area, 'query': query}
                db1['train'].save(item)
        total = rs.get('total')
        page_num = int(body.get('result').get('page_num')) + 1
        # print content
        print page_num
        print page_num * 10, total
        if page_num * 10 < total:
            next_link = '%s&pn=%d&nn=%d' % (response.url.split('&pn=')[0], page_num, page_num*10)
            print next_link
            yield Request(next_link, callback=self.parse)
