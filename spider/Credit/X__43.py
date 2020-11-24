# -*- coding: utf-8 -*-
import re

from manager.engine import Engine
import json
from fuclib import ezfuc
from parsel import Selector

from spider_code.confs import getConfig
from spider_code.items import CreditItem

gConfig = getConfig.get_config()


class Spider(Engine):
    name = 'X--43'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.url = 'http://220.160.53.3:30050/gzwz/unit/vwUnitManage/listUnit.action'
        self.detail_url = "http://220.160.53.3:30050/gzwz/creditmanage/unit/evLastArchives/getEvCreditevluation.action?orgCode={tax_id}&infoType=lianghao"
        self.data = {
            '_condition': '[]',
            '_conditionCache': '',
            '_isCount': 'true',
            '_metadata': '[{"name":"xyEpRgInfoId","hide":"true","displyName":"epId"},{"name":"unitName","displyName":"企业名称"},{"name":"orgCode","displyName":"统一社会信用代码/组织机构代码"},{"name":"legalPeople","displyName":"法定代表人"},{"name":"registerCity","displayType":"CODE","codeId":"XY_PROVINCE_CITY","displyName":"注册城市"},{"name":"orgCode","hide":"true","displyName":"组织机构代码"},{"name":"zzxx","hide":"true","displyName":"资质信息"}]',
            '_page': '1',
            '_size': '5',
            '_sort': '{"updateTime":"desc"}',
            '_total': '0',
        }
        self.total = 0
        self.total_count = 0
        self.page = 1
        self.filter_data = True

    def start_requests(self):
        self.produce(
            url=self.url,
            method='post',
            data=self.data,
        )

    def parse(self, response):
        ret = json.loads(response.text)
        result = ret['result']
        if not self.total:
            self.total = result['totalPages']
        if not self.total_count:
            self.total_count = result['totalElements']
        content_li = result['content']
        for i in content_li:
            tax_id = i['orgCode']
            tax_name = i['unitName']
            self.produce(
                url=self.detail_url.format(tax_id=tax_id),
                callback=self.parse_detail,
                meta={'name': tax_name}
            )

        while self.page < self.total:
            self.page += 1
            self.data['_page'] = str(self.page)
            self.produce(
                url=self.url,
                method='post',
                data=self.data,
                callback=self.deal_parse
            )

    def deal_parse(self, response):
        ret = json.loads(response.text)
        result = ret['result']
        content_li = result['content']
        for i in content_li:
            tax_id = i['orgCode']
            tax_name = i['unitName']
            self.produce(
                url=self.detail_url.format(tax_id=tax_id),
                callback=self.parse_detail,
                meta={'name': tax_name}
            )

    def parse_detail(self, response):
        result = json.loads(response.text)
        content_li = result['result']
        for i in content_li:
            item = CreditItem()
            item['企业名称'] = response.meta['name']
            item['网站维护代码'] = "x--43"
            item['发布日期'] = i['period']
            item['信用等级'] = i['unitLevel']
            item['url'] = response.url
            item['md5'] = ezfuc.md5(item['企业名称'], item['发布日期'], item['信用等级'])
            self.pipeline(item)


if __name__ == '__main__':
    from manager.run import run

    run(["Credit", "X__43", "auto", 1])
