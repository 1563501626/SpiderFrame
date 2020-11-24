# -*- coding: utf-8 -*-
import datetime
import re
import time

import scrapy
from spider_code.confs import getConfig
from spider_code.items import CreditItem
from fuclib import format_time
from fuclib import ezfuc
import json

# configuration item
gConfig = getConfig.get_config()


import manager
class Spider(manager.Spider):
    name = 'X--92'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': '61.152.146.213',
        'Origin': 'http://61.152.146.213',
        'Referer': 'http://61.152.146.213/CXFCX/index',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest', }
    data = {
        'page': '1',
        'rows': '15'
    }
    url = 'http://61.152.146.213/cxfcx/GetPagerIndex'
    detail_url = 'http://61.152.146.213/cxfcx/GetCXFInfo'
    download_delay = float(gConfig.sleep_time)
    total = 0

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.data,
            dont_filter=True,
            callback=self.parse,
            headers=self.headers
        )

    def parse(self, response):
        res = json.loads(response.text)
        if not self.total:
            self.total = ezfuc.toal_page(res['total'], 15)
        for i in range(1, self.total + 1):
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.data,
                dont_filter=True,
                callback=self.deal_parse,
                headers=self.headers
            )

    def deal_parse(self, response):
        res = json.loads(response.text)
        content_li = res['rows']
        for i in content_li:
            name = i['QiYeMingCheng']
            tax = i['TongYiSheHuiXYDM']
            url = f'http://61.152.146.213/cxfcx/details?qymc={name}&xydm={tax}'
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                callback=self.before_detail_parse,
                headers=self.headers,
                meta={'tax': tax}
            )

    def before_detail_parse(self, response):
        jzrq = re.search(r'var jzrq_m = "(.*?)"', response.text).group(1)
        yield scrapy.FormRequest(
            url=self.detail_url,
            headers=self.headers,
            dont_filter=True,
            callback=self.detail_parse,
            formdata={
                'jzrq': jzrq,
                'id': '',
                'xydm': response.meta['tax']
            }
        )

    def detail_parse(self, response):
        res = json.loads(response.text)
        item = res["data"]['list_score']
        item_loader = CreditItem()
        item_loader['企业名称'] = item['Enterprise_Name']
        item_loader['评价机构'] = "上海市绿化和市容(林业)工程管理信息服务平台"
        item_loader['信用得分'] = item['Score_Total']
        item_loader['评价基准日期'] = item['CreditReport_EndDate']
        item_loader['网站维护代码'] = "X--92"
        item_loader['省'] = "上海"
        item_loader['市'] = "上海"
        item_loader['网站名称'] = "上海市绿化和市容(林业)工程管理信息服务平台"
        item_loader['url'] = f"http://61.152.146.213/cxfcx/details?qymc={item_loader['企业名称']}&xydm={item['Enterprise_tyshxydm']}"

        yield item_loader
        # print(dict(item_loader))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--92'.split())
