# -*- coding: utf-8 -*-
import scrapy
from spider_code.api import hj_tools as eamonn
from spider_code.confs import getConfig
from spider_code.items import AutoItem
gConfig = getConfig.get_config()


import manager
class X75Spider(manager.Spider):
    name = 'X--77'
    download_delay = float(gConfig.sleep_time)

    def __init__(self, *args, **kwargs):
        super(X75Spider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://121.33.200.110:8088/evaluateCompanyResult/load_result_public_list?isShow=1&_search=false&nd=1594170663342&rows=10&page=1&sidx=&sord=desc&companyName=&nowGrade=&companyType=&industry=2"]
        self.url = "http://121.33.200.110:8088/evaluateCompanyResult/load_result_public_list?isShow=1&_search=false&nd=1594170663342&rows=10&page={page}&sidx=&sord=desc&companyName=&nowGrade=&companyType=&industry=2"
        self.total = 0
        self.page = 1

    def parse(self, response):
        _, res = eamonn.ex(response.text, ex='json')
        if not self.total:
            self.total = int(res['total'])

        trs = res['rows']
        for tr in trs:
            item_loader = AutoItem()
            item_loader['企业名称'] = tr['company_name']
            item_loader['工程类型'] = tr['industry_name']
            item_loader['企业类型'] = tr['company_type_name']
            item_loader['年份'] = tr['year']
            item_loader['信用等级'] = tr['now_grade']
            item_loader['评价机构'] = "广东省交通建设市场信用管理系统"
            item_loader['网站维护代码'] = "x--77"
            item_loader['网站名称'] = "广东省交通建设市场信用管理系统"
            item_loader['url'] = response.url

            yield item_loader
            # print(item_loader)

        self.page += 1
        if self.page <= self.total:
            yield scrapy.Request(
                url=self.url.format(page=self.page),
                dont_filter=True
            )


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--77'.split())
