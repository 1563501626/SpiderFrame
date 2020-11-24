# -*- coding: utf-8 -*-
import datetime
import scrapy
from spider_code.confs import getConfig
from spider_code.items import AutoItem, CreditItem
from fuclib import ezfuc
import manager

# configuration item
gConfig = getConfig.get_config()


class Spider(manager.Spider):
    name = 'X--100'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'cxpj.ahhrit.com:9009',
        'Origin': 'http://cxpj.ahhrit.com:9009',
        'Referer': 'http://cxpj.ahhrit.com:9009/cxpj/rankingList.html?ranking=sg',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',}
    data = {
       'companyName': '',
        'pageNum': '1',
        'type': '1',
    }
    total = 0
    url = 'http://cxpj.ahhrit.com:9009/tlyl-api/company/mh/rankList'

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.data,
            headers=self.headers
        )

    def parse(self, response):
        res = response.json
        if not self.total:
            self.total = int(res['data']['pages'])
        for i in range(1, self.total + 1):
            self.data['pageNum'] = str(i)
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.data,
                callback=self.deal_parse,
                dont_filter=True,
                headers=self.headers
            )

    def deal_parse(self, response):
        res = response.json
        data = res['data']['list']
        for i in data:
            item = CreditItem()
            item['企业名称'] = i['companyName']
            item['评价机构'] = "铜陵市园林绿化企业诚信综合评价信息系统"
            item['信用得分'] = i['countsValue']['sumBuildPlus']
            item['排名'] = int(i['countsValue']['totalBuildLranking'])
            item['网站维护代码'] = "x--100"
            item['省'] = "安徽"
            item['市'] = "铜陵"
            item['网站名称'] = "铜陵市园林绿化企业诚信综合评价信息系统"
            item['url'] = response.url
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--100', 'auto', 1])
