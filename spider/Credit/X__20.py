# -*- coding: utf-8 -*-
import scrapy
import re
from fuclib import ezfuc
from spider_code.items import CreditItem


import manager
class Spider(manager.Spider):
    name = 'X--20'
    start_urls = [
        "http://pt.cdcin.com/qyxx/qyxx_kcsj.do?flmbh=66&flmmc=WoZ9gRd5LaF1RQnYeqm56A&lmbh=106&lmmc=WuxXBqGZR23Co8SSQ6Hgug&curPage=-1"
    ]
    # filter_data = True
    get_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Host": "pt.cdcin.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }

    def parse(self, response):
        url_ = re.search(r'location\.replace\("(.*?)"', response.text).group(1)
        pageCount = re.search(r"pageCount=(\d+)&", url_).group(1)
        for i in range(1, int(pageCount) + 1):
            self.get_headers['User-Agent'] = ezfuc.random_ua()
            url = url_ + str(i)
            yield scrapy.Request(
                url=url,
                headers=self.get_headers,
                dont_filter=True,
                callback=self.get_sgdata
            )

    def get_sgdata(self, response):
        tr_list = response.xpath('//table[@class="table-style1"]/tr[position()>1]')
        for i in tr_list:
            item = CreditItem()
            item['企业名称'] = i.xpath('td[1]/@title').extract_first('')
            item['评价机构'] = "成都建信企业信息"
            item['网站维护代码'] = self.name
            item['省'] = "四川"
            item['市'] = "成都"
            item['网站名称'] = "成都建信"
            item['url'] = response.url
            # item['md5'] = ezfuc.md5([item['企业名称'], item['评价机构'], item['省'], item['市'], item['网站名称']])
            yield item
            # print(dict(item))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl X--20".split())
