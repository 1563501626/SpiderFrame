# -*- coding: utf-8 -*-
import copy
import json
import time

import scrapy
from spider_code.confs import getConfig
from spider_code.items import AutoItem, CreditItem
from fuclib import ezfuc
import manager

# configuration item
gConfig = getConfig.get_config()


class Spider(manager.Spider):
    name = 'X--126'
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
    url = 'http://49.65.0.83/ProjectRegister/DisplayWebs/Ashx/GetKCCreditInfo.ashx'

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.data,
            headers=self.headers,
        )

    def parse(self, response):
        res = response.json
        if not self.total:
            self.total = ezfuc.toal_page(res['count'], 10)
        for i in range(self.total):
            self.data['PageIndex'] = str(i)
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.data,
                callback=self.deal_parse,
                dont_filter=True,
                headers=self.headers,
                meta={'page': i}
            )

    def deal_parse(self, response):
        # res = response.json
        time.sleep(2)
        try:
            res = response.json
        except:
            self.data['PageIndex'] = str(response.meta['page'])
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.data,
                callback=self.deal_parse,
                dont_filter=True,
                headers=self.headers,
                meta={'page': response.meta['page']}
            )
            return
        data = res['list']
        for i in data:
            item = CreditItem()
            item['企业名称'] = i['EntName']
            item['评价机构'] = '南克市建筑市场监管诚值信思一体化平台'
            item['评价年度'] = i['KaoPingND']
            item['信用等级'] = i['KaoPingDJ']
            item['网站维护代码'] = 'X--126'
            item['省'] = '江苏'
            item['市'] = '南京'
            item['网站名称'] = '南克市建筑市场监管诚值信思一体化平台'
            item['url'] = self.url
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--126', 'w', 1])
