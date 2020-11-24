# -*- coding: utf-8 -*-
import scrapy
import time
from random import randint

from fuclib import ezfuc

from spider_code.items import CreditItem

now_time = time.strftime("%F")


import manager
class Spider(manager.Spider):
    name = 'X--35'
    filter_data = True
    allowed_domains = ['http://220.160.52.164:98']
    start_urls = [
        f'http://220.160.52.164:98/zjxypj/zjxypjform/homepage/ALLEvaluate/CSEPALLEvaluateMain_n.aspx?nowtime={now_time}']
    post_data = {
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATEENCRYPTED": "",
        "head1$nowtime": str(now_time),
        "id": "",
        "datetime": "",
        "FSTYPE": "",
        "txtcsepname": "",
        "txtcsepcode": "",
        "txtSCOREDATE": str(now_time),
    }

    def parse(self, response):
        items = {
            # "X--37": "RadFSTYPE2",
            # "X--36": "RadFSTYPE3",
            "X--35": "RadFSTYPE1"
        }
        for website_code, a in items.items():
            self.post_data['__VIEWSTATE'] = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first('')
            self.post_data['__VIEWSTATEGENERATOR'] = response.xpath(
                '//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first('')
            self.post_data['__EVENTVALIDATION'] = response.xpath(
                '//input[@id="__EVENTVALIDATION"]/@value').extract_first('')
            self.post_data['ddl'] = '1'
            self.post_data['a'] = a
            self.post_data['__EVENTTARGET'] = 'linkBtnQuery'
            yield scrapy.FormRequest(
                url=response.url,
                meta={"a": a, "website_code": website_code, "pageNo": 1},
                formdata=self.post_data,
                dont_filter=True,
                callback=self.ListData
            )

    def ListData(self, response):
        website_code = response.meta['website_code']
        pageNo = response.meta['pageNo']
        a = response.meta['a']
        items = response.xpath('//table/tr[position()>1]')
        for it in items:
            企业名称 = it.xpath('td[2]/span/@title').extract_first('')
            score = it.xpath('td[8]/text()').extract_first('')
            calculate_date = it.xpath('td[9]/text()').extract_first('')
            ranking = it.xpath('td[1]/text()').extract_first('')
            _id = it.xpath('td[10]/input/@name').extract_first('')
            detail_post_data = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATEENCRYPTED": "",
                "head1$nowtime": str(now_time),
                "id": "",
                "datetime": "",
                "FSTYPE": "",
                "txtcsepname": "",
                "txtcsepcode": "",
                "txtSCOREDATE": str(now_time),
                _id + '.y': str(randint(1, 100)),
                _id + '.x': str(randint(1, 100)),
                '__VIEWSTATE': response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first(''),
                '__VIEWSTATEGENERATOR': response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first(''),
                '__EVENTVALIDATION': response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first(''),
                'ddl': str(pageNo),
                'a': a,
            }
            yield scrapy.FormRequest(
                url=response.url,
                meta={"calculate_date": calculate_date, "website_code": website_code, "score": score, "企业名称": 企业名称,
                      "ranking": ranking},
                formdata=detail_post_data,
                dont_filter=True,
                callback=self.detailList
            )

        page_num = response.xpath('string(//span[@id="lblpagecount"])').extract_first('').strip()
        if pageNo < int(page_num):
            pageNo += 1
            self.post_data['__VIEWSTATE'] = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first('')
            self.post_data['__VIEWSTATEGENERATOR'] = response.xpath(
                '//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first('')
            self.post_data['__EVENTVALIDATION'] = response.xpath(
                '//input[@id="__EVENTVALIDATION"]/@value').extract_first('')
            self.post_data['ddl'] = str(pageNo - 1)
            self.post_data['a'] = a
            self.post_data['__EVENTTARGET'] = 'lbNext'
            yield scrapy.FormRequest(
                url=response.url,
                meta={"a": a, "website_code": website_code, "pageNo": pageNo},
                formdata=self.post_data,
                dont_filter=True,
                callback=self.ListData
            )

    def detailList(self, response):
        企业名称 = response.meta['企业名称']
        评价机构 = "福建省建筑施工企业信用综合评价系统"
        行业 = ""
        专业 = ""
        信用得分 = ''
        信用等级 = ""
        排名 = ''
        今日得分 = response.meta['score']
        今日排名 = response.meta['ranking']
        六十得分 = ''
        六十日排名 = ''
        评价年度 = ""
        网站维护代码 = response.meta['website_code']
        发布日期 = response.meta['calculate_date']
        有效期 = ""
        省 = "福建"
        市 = "福建"
        网站名称 = "福建省建筑施工企业信用综合评价系统"
        encode_md5 = ezfuc.md5(网站名称, 企业名称, 信用等级, 发布日期, response.url, time.strftime("%F"))
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
        item['md5'] = encode_md5
        yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--35', 'auto', 1])
