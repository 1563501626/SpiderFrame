# -*- coding: utf-8 -*-
import datetime

import scrapy
from fuclib import ezfuc
from spider_code.confs import getConfig
from spider_code.items import AutoItem
import pandas as pd
import re
import math


import manager
class Spider(manager.Spider):
    name = 'R--34'
    data = {'pageNo': '1', 'pageSize': '20', 'staffName': '', 'unitName': '', 'creditNum': '', 'staffType': '1',
            'engineerNum': ''}
    total = 0
    page = 1
    db = getConfig.conn("zlcollector_credit")
    url = "http://114.251.10.92:8080/XYPT/staff/openList"

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.data,
            dont_filter=True,
            callback=self.parse
        )

    def parse(self, response):
        if not self.total:
            self.total = math.ceil(int(re.search(r"共\s*(\d+)\s*条", response.text).group(1)) / 20)
        trs = response.xpath("//table[@id='contentTable']/tbody/tr")
        for i in trs:
            item = {}
            item['姓名'] = i.xpath("string(./td[2])").extract_first("").strip()
            item['公司名称'] = i.xpath("string(./td[3])").extract_first("").strip()
            item['证书级别'] = i.xpath("string(./td[4])").extract_first("").strip()
            item['注册证书编号'] = i.xpath("string(./td[5])").extract_first("").strip()
            if "e" in item['注册证书编号']:
                print()
            item['人员状态'] = i.xpath("string(./td[8])").extract_first("").strip()
            item['发证时间'] = i.xpath("string(./td[9])").extract_first("").strip()
            item['网站代码'] = 'R--34'
            item['省市'] = '国家'
            item['网站名称'] = '环境影响评价信用平台'
            item['注册类型及等级'] = '环境影响评价师'
            item['网站Url'] = self.url
            item['新增md5'] = ezfuc.md5(
                item['姓名'],
                item['公司名称'],
                item['注册证书编号'],
                item['发证时间'],
                item['注册类型及等级']
            )
            item['注销md5'] = ezfuc.md5(
                item['姓名'],
                item['公司名称'],
                item['注册证书编号'],
                item['注册类型及等级']
            )
            q = self.db.query("select 新增md5 from r__34 where 新增md5='%s'" % item['新增md5'])
            if not q:
                item['采集时间'] = datetime.datetime.now().strftime('%F %H:%M:%S')
                self.db.insert("r__34", item)
                print(item)
            else:
                print("数据重复.")
                pass
                z = self.db.query("select id, 注销md5 from r__34 where 注销md5='%s'" % item['注销md5'])
                if z:
                    for ii in z:
                        sql = "update r__34 set 采集时间='%s' where id=%s" % (
                            datetime.datetime.now().strftime('%F %H:%M:%S'), ii['id'])
                        print(sql)
                        self.db.query(sql)

        self.page += 1
        if self.page <= self.total:
            self.data['pageNo'] = str(self.page)
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.data
            )


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl R--34'.split())
