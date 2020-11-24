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
    name = 'X--108'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'xy.cacem.com.cn',
        'Origin': 'http://xy.cacem.com.cn',
        'Referer': 'http://xy.cacem.com.cn/creditrating.html?&p=2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',}
    data = {
        'pageNumber': '1',
        'pageSize': '10'
    }
    total = 0
    cookie = {}
    url = 'http://xy.cacem.com.cn/jf/itf/entGradingResult/list_xypjcx/'

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.data,
            headers=self.headers,
        )

    def parse(self, response):
        res = response.json
        if not self.total:
            self.total = int(res['Data']['totalPage'])
        for i in range(1, self.total + 1):
            self.data['pageNumber'] = str(i)
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.data,
                callback=self.deal_parse,
                dont_filter=True,
                headers=self.headers
            )

    def deal_parse(self, response):
        res = response.json
        data = res['Data']['list']
        for i in data:
            item = CreditItem()
            item['企业名称'] = i['enterprise_name']
            item['评价机构'] = '工程建设行业信用体系建设平台'
            item['信用等级'] = i['credit_rating']
            item['评价年度'] = i['year']
            item['网站维护代码'] = 'X--108'
            item['发布日期'] = i['issue_date']
            item['有效期'] = i['valid_until']
            item['省'] = '全国'
            item['市'] = '全国'
            item['网站名称'] = '工程建设行业信用体系建设平台'
            item['url'] = 'http://xy.cacem.com.cn/creditrating.html?&p=1'
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--108', 'auto', 1])
