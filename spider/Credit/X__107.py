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
    name = 'X--107'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': 'Bearer 1d250e311107f86b33444adf3fb46edc',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'ggzy.huangshan.gov.cn',
        'Origin': 'http://ggzy.huangshan.gov.cn',
        'Referer': 'http://ggzy.huangshan.gov.cn/xyjl/018002/subpagexyxxhmd.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'}
    data = '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","UNITORGNUM":"","DANWEINAME":"","CURRENTPAGEINDEX":%s,"PAGESIZE":12}'
    total = 0
    cookie = {}
    url = 'http://ggzy.huangshan.gov.cn/EpointWebBuilder/rest/getxyjl/getallcompany'

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            formdata={'params': self.data % 0},
            headers=self.headers,
        )

    def parse(self, response):

        if not self.total:
            self.total = ezfuc.toal_page(response.json['TOTALNUM'], 12)
        for i in range(self.total):
            yield scrapy.FormRequest(
                url=self.url,
                formdata={'params': self.data % i},
                callback=self.deal_parse,
                dont_filter=True,
                headers=self.headers
            )

    def deal_parse(self, response):
        res = json.loads(response.json['RETURNDATA'])
        data = res
        for i in data:
            item = CreditItem()
            item['企业名称'] = i['danweiname']
            item['评价机构'] = "黄山市公共资源交易竞争主体信用信息管理部门"
            item['信用得分'] = i['lastscore']
            item['网站维护代码'] = "x--107"
            item['省'] = "安徽"
            item['市'] = "黄山"
            item['网站名称'] = "黄山市公共资源交易中心"
            item['url'] = 'http://ggzy.huangshan.gov.cn/xyjl/018002/subpagexyxxhmd.html'
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--107', 'w', 1])
