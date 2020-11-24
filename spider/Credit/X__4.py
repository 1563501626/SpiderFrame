# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json
from math import ceil
import time

from fuclib import ezfuc

import manager
from spider_code.items import AutoItem


class Spider(manager.Spider):
    name = 'X--4'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'glxy.mot.gov.cn',
        'Origin': 'https://glxy.mot.gov.cn',
        'Referer': 'https://glxy.mot.gov.cn/evaluate/index.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    post_data = {
        'page': '1',
        'rows': '15',
        'type': '0',
        'name': '',
        'oeriodCode': '',
        'evaGrade': '',
        'provinceCode': '',
    }
    url = 'https://glxy.mot.gov.cn/evaluate/getEvaluateList.do'

    def start_requests(self):
        for i in ['0', '2']:  # 0：施工 1：设计
            self.post_data['type'] = i
            yield scrapy.FormRequest(
                url=self.url,
                headers=self.headers,
                formdata=self.post_data,
                meta={'type': i}
            )

    def parse(self, response):
        t = response.meta['type']
        res = json.loads(response.text)
        total_page = int(res['pageObj']['maxPage'])
        for i in range(1, total_page + 1):
            self.post_data['type'] = t
            self.post_data['page'] = str(i)
            yield scrapy.FormRequest(
                url=self.url,
                headers=self.headers,
                formdata=self.post_data,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        items = json.loads(response.text)['rows']
        for it in items:
            企业名称 = it['corpName']
            评价机构 = "全国公路建设市场信用信息管理系统"
            行业 = ''
            专业 = it['companyType']
            信用得分 = it['doScore']
            信用等级 = it['evaGrade']
            排名 = ''
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = it['oeriodCode']
            网站维护代码 = 'X--4'
            发布日期 = ''
            有效期 = ""
            省 = "国家"
            市 = ""
            网站名称 = "全国公路建设市场信用信息管理系统"
            item = AutoItem()
            item['企业名称'] = 企业名称
            item['评价机构'] = 评价机构
            item['行业'] = 行业
            item['专业'] = 专业
            item['信用得分'] = 信用得分
            item['信用等级'] = 信用等级
            item['排名'] = 排名
            item['今日得分'] = 今日得分
            item['今日排名'] = 今日排名
            item['六十日得分'] = 六十得分
            item['六十日排名'] = 六十日排名
            item['评价年度'] = 评价年度
            item['网站维护代码'] = 网站维护代码
            item['发布日期'] = 发布日期
            item['有效期'] = 有效期
            item['省'] = 省
            item['市'] = 市
            item['网站名称'] = 网站名称
            item['url'] = response.url
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--4', 'auto', 1])
