# -*- coding: utf-8 -*-
import hashlib

import scrapy, md5
from scrapy.http import Request
from scrapy.selector import Selector
from school_list.items import SchoolListItem


class SchoolSpider(scrapy.Spider):
    name = "school"
    allowed_domains = ["xuexiao.51sxue.com"]
    t_arr = [1, 2, 3, 4, 5, 6]
    p_arr = [11, 12, 13, 14, 21, 22, 23, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 50, 51, 52, 53, 61, 62, 63, 64, 65]
    start_urls = []
    for t in t_arr:
        for p in p_arr:
            start_urls.append("http://xuexiao.51sxue.com/slist/?t=%d&areaCodeS=%d&page=1" % (t, p))
    # start_urls.append("http://xuexiao.51sxue.com/slist/?t=1&areaCodeS=11&page=1")

    print start_urls

    def parse(self, response):
        # print response.body
        item = SchoolListItem()
        selector = Selector(response)
        schooles = selector.xpath('//div[@class="reply_box"]')
        for s in schooles:
            name = s.xpath('descendant::li[1]/h3/a/text()').extract()[0]
            desc = ''
            icon = s.xpath('descendant::a[1]/img/@src').extract()
            icon = icon[0] if icon else ''
            address = s.xpath('ul[@class="school_m_lx"]/li[@class="school_dz"]/b/text()').extract()
            address = address[0] if address else ''
            tell = s.xpath('ul[@class="school_m_lx"]/li[@class="school_telephone"]/b/text()').extract()
            tell = tell[0] if tell else ''
            area = s.xpath('descendant::li[2]/b/text()').extract()[0]
            type = s.xpath('descendant::li[4]/ol[2]/b/text()').extract()[0]
            attr = s.xpath('descendant::li[3]/b/text()').extract()
            attr = attr[0] if attr else ''
            nature = s.xpath('descendant::li[4]/ol[1]/b/text()').extract()
            nature = nature[0] if nature else ''
            url = s.xpath('descendant::li[1]/h3/a/@href').extract()[0]
            score = s.xpath('div[@class="school_t_con"]/div[@class="school_m_df fl"]/div[@class="school_m_tu"]/img/@src').extract()[0]
            comment = s.xpath('div[@class="school_con_w"]/text()').extract()
            comment = comment[0] if comment else ''
            score_count = s.xpath('div[@class="school_t_con"]/div[@class="school_m_df fl"]/div[@class="school_m_text"]/b/text()').extract()[0]
            province = selector.xpath('//li[@class="school_szd"]/text()').extract()[0]

            m = hashlib.md5()
            m.update(name.encode('utf-8'))
            item['_id'] = m.hexdigest()
            item['name'] = name
            item['icon'] = icon
            item['address'] = address
            item['tell'] = tell
            item['area'] = area
            item['type'] = type
            item['attr'] = attr
            item['nature'] = nature
            item['url'] = url
            item['score'] = score
            item['comment'] = comment
            item['score_count'] = score_count
            item['province'] = province
            yield item

        page_hover = selector.xpath('//a[@class="page_hover"]/text()').extract()
        total = selector.xpath('//div[@class="page mtr10"]/span[@class="down"]/text()').extract()
        page_hover = page_hover[0] if page_hover else ''
        total = total[0] if total else ''
        if total and int(page_hover) < int(total[1:]):
            next_link = '%s&page=%d' % (response.url.split('&page=')[0], int(page_hover)+1)
            print next_link
            yield Request(next_link, callback=self.parse)

