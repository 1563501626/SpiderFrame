# -*- coding: utf-8 -*-
import copy
import json

import scrapy
from spider_code.confs import getConfig
from spider_code.items import AutoItem, CreditItem
from fuclib import ezfuc
import manager

# configuration item
gConfig = getConfig.get_config()


class Spider(manager.Spider):
    name = 'X--109'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',}
    data = {
        'pageNumber': '1',
        'pageSize': '10'
    }
    total = 0
    cookie = {}
    url = 'http://www.cscgov.cn/col.jsp?id=112'

    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            headers=self.headers,
        )

    def parse(self, response):
        res = response.xpath("//div[@id='productTextList502']/table")
        for i in res:
            item = CreditItem()
            item['企业名称'] = i.xpath(".//a/@title").extract_first("").strip()
            item['评价机构'] = '全国商务诚信公示平台'
            item['信用等级'] = i.xpath(".//span[@class='propValue']/text()").extract_first("").strip()
            item['网站维护代码'] = 'X--109'
            item['省'] = '全国'
            item['市'] = '全国'
            item['网站名称'] = '全国商务诚信公示平台'
            item['url'] = response.urljoin(i.xpath(".//a/@href").extract_first(""))
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--109', 'auto', 1])
