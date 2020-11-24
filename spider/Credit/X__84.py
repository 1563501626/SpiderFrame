# -*- coding: utf-8 -*-
import re

from manager.engine import Engine
import json
from spider_code.api import hj_tools as eamonn
from parsel import Selector

from spider_code.confs import getConfig
from spider_code.items import CreditItem

gConfig = getConfig.get_config()


class Spider(Engine):
    name = 'X--84'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.url = 'http://223.244.255.14/ent/businessList'
        self.headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Host': '223.244.255.14',
                        'Origin': 'http://223.244.255.14',
                        'Referer': 'http://223.244.255.14/ent/',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest',}
        self.data = {
            'scoreType': '1',
            'evaluateType': '0',
            'searchValue': '',
            'pageNum': '1',
            'pageSize': '10',
        }
        # self.proxy = True
        self.total = 0
        self.total_count = 0
        self.page = 1

    def start_requests(self):
        self.produce(
            url="http://223.244.255.14/ent/",
            headers=self.headers,
            callback=self.before_parse
        )

    def before_parse(self, response):
        self.headers['Cookie'] = f'JSESSIONID={response.res.cookies.get("JSESSIONID").value}'
        csrf = re.search(r'_csrf.token = "(.*?)"', response.text).group(1)
        self.headers['X-CSRF-TOKEN'] = csrf
        self.produce(
            url=self.url,
            method='post',
            data=self.data,
            headers=self.headers
        )

    def parse(self, response):
        result = json.loads(response.text)
        if not self.total:
            self.total = eamonn.page(result['total'], 10)
        if not self.total_count:
            self.total_count = result['total']
        content_li = result['rows']
        for i in content_li:
            item = CreditItem()
            item['企业名称'] = i['ENTNAME']
            item['评价机构'] = "滁州市建筑市场信用管理系统"
            item['信用得分'] = i['EVALUATESCORE']
            item['网站维护代码'] = "x--84"
            item['发布日期'] = i['CREATETIME']
            item['省'] = "安徽"
            item['市'] = "滁州"
            item['网站名称'] = "滁州市建筑市场信用管理系统"
            item['url'] = self.url
            self.pipeline(item)

        while self.page < self.total:
            self.page += 1
            self.data['pageNum'] = str(self.page)
            self.produce(
                url=self.url,
                method='post',
                data=self.data,
                headers=self.headers,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        result = json.loads(response.text)
        content_li = result['rows']
        for i in content_li:
            item = CreditItem()
            item['企业名称'] = i['ENTNAME']
            item['评价机构'] = "滁州市建筑市场信用管理系统"
            item['信用得分'] = i['EVALUATESCORE']
            item['网站维护代码'] = "x--84"
            item['发布日期'] = i['CREATETIME']
            item['省'] = "安徽"
            item['市'] = "滁州"
            item['网站名称'] = "滁州市建筑市场信用管理系统"
            item['url'] = self.url
            self.pipeline(item)


if __name__ == '__main__':
    from manager.run import run

    run(['Credit', 'X--84', 'auto', 1])
