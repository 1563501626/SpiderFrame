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
    name = 'X--121'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': '49.65.0.83',
        'Origin': 'http://49.65.0.83',
        'Referer': 'http://49.65.0.83/ProjectRegister/DisplayWebs/Pages/EntCreditInfo/SGCreditInfo/SGCreditInfo_List.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',}
    data = {
        'AppendCondition': '',
        'PageIndex': '1',
        'PageSize': '10',
        'Condition': '',
    }
    total = 0
    cookie = {}
    url = 'http://60.173.0.184:8808/credit/public/sgScoreList?currentPage=%s&limit=10'

    def start_requests(self):
        yield scrapy.Request(
            url=self.url % 1,
            headers=self.headers,
        )

    def parse(self, response):
        res = response.json
        if not self.total:
            self.total = ezfuc.toal_page(res['count'], 10)
        for i in range(self.total):
            yield scrapy.Request(
                url=self.url % i,
                callback=self.deal_parse,
                dont_filter=True,
                headers=self.headers
            )

    def deal_parse(self, response):
        res = response.json
        data = res['data']
        for i in data:
            item = CreditItem()
            item['企业名称'] = i['compName']
            item['评价机构'] = '铜陵市建筑施工企业和房地产开发企业信用系统'
            item['网站维护代码'] = 'X--121'
            item['信用得分'] = i['score']
            item['省'] = '安徽'
            item['市'] = '铜陵'
            item['网站名称'] = '铜陵市建筑施工企业和房地产开发企业信用系统'
            item['url'] = 'http://60.173.0.184:8808/credit/public/sgList'
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--121', 'auto', 1])
