# -*- coding: utf-8 -*-
import scrapy
import time

from fuclib import ezfuc

from spider_code.items import AutoItem

now_time = time.strftime("%F")
from datetime import datetime


def m(m):
    if m in ["2", '3', '4']:
        return "第一季度"
    elif m in ["5", '6', '7']:
        return "第二季度"
    elif m in ["8", '9', '10']:
        return "第三季度"
    else:
        return "第四季度"


import manager
class Spider(manager.Spider):
    name = 'X--38'
    filter_data = True
    allowed_domains = ['http://220.160.52.164:98']
    start_urls = ['http://220.160.52.164:98/zjxypj/zjxypjform/homepage/ALLEvaluate/CSEPALLEvaluateMain_Quarter.aspx']
    post_data = {
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATEENCRYPTED": "",
        "head2$nowtime": str(now_time),
        "id": "",
        "datetime": "",
        "FSTYPE": "",
        "txtcsepname": "",
        "txtcsepcode": "",
        # "txtqu":m(datetime.now().strftime("%m")).encode("gb2312"),
        "txtsyear": datetime.now().strftime("%Y"),
    }
    page_num = 0

    def parse(self, response):
        items = {
            "X--38": "RadFSTYPE1"
        }
        month = datetime.now().month
        jd_L = []
        if 3 <= month < 6:
            jd_L.append("第一季度")
        elif 6 <= month < 9:
            jd_L.append("第二季度")
        elif 9 <= month < 12:
            jd_L.append("第三季度")
        else:
            jd_L.append("第四季度")

        n_L = {
            # "2015",
            # "2016",
            # "2017",
            # "2018",
            # "2019",
            str(datetime.now().year-1) if 1 <= month < 3 else str(datetime.now().year)
        }
        for website_code, a in items.items():
            for txtqu in jd_L:

                for txtsyear in n_L:
                    self.post_data['__VIEWSTATE'] = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first(
                        '')
                    self.post_data['__VIEWSTATEGENERATOR'] = response.xpath(
                        '//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first('')
                    self.post_data['__EVENTVALIDATION'] = response.xpath(
                        '//input[@id="__EVENTVALIDATION"]/@value').extract_first('')
                    self.post_data['ddl'] = '1'
                    self.post_data['a'] = a
                    self.post_data['__EVENTTARGET'] = 'linkBtnQuery'
                    self.post_data['txtqu'] = txtqu.encode('gb2312')
                    self.post_data['txtsyear'] = txtsyear
                    yield scrapy.FormRequest(
                        url=response.url,
                        method="POST",
                        meta={"a": a, "website_code": website_code, "pageNo": 1, "txtsyear": txtsyear, "txtqu": txtqu},
                        formdata=self.post_data,
                        dont_filter=True,
                        callback=self.ListData
                    )

    def ListData(self, response):
        website_code = response.meta['website_code']
        pageNo = response.meta['pageNo']
        txtqu = response.meta['txtqu']
        txtsyear = response.meta['txtsyear']
        a = response.meta['a']
        items = response.xpath('//table/tr[position()>1]')
        for it in items:
            排名 = it.xpath('td[1]/text()').extract_first('')
            if '没有记录' != 排名:
                企业名称 = it.xpath('td[2]/span/@title').extract_first('')
                评价机构 = "福建省建筑施工企业信用综合评价系统"
                行业 = ""
                专业 = ""
                信用得分 = it.xpath('td[8]/text()').extract_first('')
                信用等级 = ""
                今日得分 = ''
                今日排名 = ''
                六十得分 = ''
                六十日排名 = ''
                评价年度 = it.xpath('td[10]/text()').extract_first('') + f"，{txtqu}"
                网站维护代码 = response.meta['website_code']
                发布日期 = ''
                有效期 = ""
                省 = "福建"
                市 = "福建"
                网站名称 = "福建省建筑施工企业信用综合评价系统"
                encode_md5 = ezfuc.md5(网站名称, 企业名称, 信用得分, response.url, 评价年度)
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
                item['md5'] = encode_md5
                yield item

        if not self.page_num:
            self.page_num = response.xpath('//span[@id="lblpagecount"]/font/text()').extract_first('').strip()
        if pageNo < int(self.page_num):
            pageNo += 1
            self.post_data['__VIEWSTATE'] = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first('')
            self.post_data['__VIEWSTATEGENERATOR'] = response.xpath(
                '//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first('')
            self.post_data['__EVENTVALIDATION'] = response.xpath(
                '//input[@id="__EVENTVALIDATION"]/@value').extract_first('')
            self.post_data['ddl'] = str(pageNo - 1)
            self.post_data['a'] = a
            self.post_data['txtqu'] = txtqu.encode('gb2312')
            self.post_data['txtsyear'] = txtsyear
            self.post_data['__EVENTTARGET'] = 'lbNext'
            yield scrapy.FormRequest(
                url=response.url,
                meta={"a": a, "website_code": website_code, "pageNo": pageNo, "txtsyear": txtsyear, "txtqu": txtqu},
                formdata=self.post_data,
                dont_filter=True,
                callback=self.ListData
            )


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--38', 'auto', 1])
