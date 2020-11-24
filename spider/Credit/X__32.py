# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json
from math import ceil
import time

from fuclib import ezfuc

import manager
from spider_code.items import CreditItem


class Spider(manager.Spider):
    name = 'X--32'
    allowed_domains = ['http://218.2.208.148:8084']
    start_urls = ['http://http://218.2.208.148:8084/']
    z_dict = {
        "1": "施工单位",
        "2": "监理单位",
        "3": "勘察设计",
        "4": "试验检测单位",
        "5": "材料采购单位",
        "7": "其他咨询服务",
        "8": "工程审计和造价咨询",
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'security_session_verify=d239d6b5daa8bef436389584c11c7d53; JSESSIONID=4e935e40-4768-4123-b104-80a5d58f1a11',
        'Host': '218.2.208.148:8282',
        'Origin': 'http://218.2.208.148:8282',
        'Referer': 'http://218.2.208.148:8282/cims/publicity/toCredit',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    post_data = {
        'year': '2019',
        'season': '信用评价',
        'enterpriseType': '1',
        'credit': '',
        'enterpriseName2': '',
        'fkEnterpriseId': '',
        'pageSize': '10',
        'pageNum': '1',
        'orderByColumn': '',
        'isAsc': 'asc',
    }
    url = 'http://218.2.208.148:8282/cims/publicity/creditRecordList'

    def start_requests(self):
        url = "http://218.2.208.148:8282/cims/publicity/creditRecordList"
        yield scrapy.FormRequest(
            url=url,
            meta={"pageN0": 1},
            formdata=self.post_data,
            dont_filter=True
        )

    def parse(self, response):
        items = json.loads(response.text)['rows']
        for it in items:
            企业名称 = it['enterpriseName']
            评价机构 = "江苏省公路水路建设市场"
            行业 = ""
            专业 = self.z_dict[it['enterpriseType']]
            信用得分 = it['creditScore']
            信用等级 = it['credit']
            排名 = ''
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = it['year']
            网站维护代码 = 'X--32'
            发布日期 = ''
            有效期 = ""
            省 = "江苏"
            市 = "江苏"
            网站名称 = "江苏省公路水路建设市场信用信息服务系统"
            item = CreditItem()
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
        total = json.loads(response.text)['total']
        page_num = ezfuc.toal_page(total, 10)
        pageN0 = response.meta['pageN0']
        if pageN0<page_num:
            pageN0 +=1
            self.post_data['pageNum'] = str(pageN0)
            yield scrapy.FormRequest(
                url=response.url,
                meta={"pageN0": pageN0},
                formdata=self.post_data,
                dont_filter=True
            )


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--32', 'w', 1])