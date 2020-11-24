# -*- coding: utf-8 -*-
import datetime
import time

import scrapy
from spider_code.confs import getConfig
from spider_code.items import AutoItem, CreditItem
from fuclib import ezfuc
import manager

# configuration item
gConfig = getConfig.get_config()


class Spider(manager.Spider):
    name = 'X--99'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '47.92.228.5:10110',
        'Origin': 'http://47.92.228.5',
        'Referer': 'http://47.92.228.5/',
        'serverName': 'suzhou-api',
        'token': 'null',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',}
    data = {"score_type": '2', "currentPage": '1', "pageSize": '10'}
    total = 0
    url = 'http://47.92.228.5:10110/suzhou-api/public/gov-admin-area-key/select-credit-list'

    def start_requests(self):
        self.produce(
            url=self.url,
            json=self.data,
            method='post',
            headers=self.headers
        )

    def parse(self, response):
        res = response.json
        if not self.total:
            self.total = ezfuc.toal_page(res['data']['pageInfo']['total'], 10)
        for i in range(1, self.total + 1):
            self.data['currentPage'] = str(i)
            self.produce(
                url=self.url,
                json=self.data,
                method='post',
                callback=self.deal_parse,
                headers=self.headers
            )

    def deal_parse(self, response):
        res = response.json
        data = res['data']['pageInfo']['list']
        for i in data:
            item = CreditItem()
            item['企业名称'] = i['corp_name']
            item['评价机构'] = "宿州市建设行业监管综合服务平台"
            item['信用得分'] = i['score']
            item['评价年度'] = time.strftime("%F", time.localtime(int(i['scoring_time']) // 1000))
            item['网站维护代码'] = "x--99"
            item['省'] = "安徽"
            item['市'] = "宿州"
            item['网站名称'] = "宿州市建设行业监管综合服务平台"
            item['url'] = response.url
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--99', 'auto', 1])
