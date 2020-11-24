# -*- coding: utf-8 -*-
import scrapy
from spider_code.items import CreditItem
import time
from fuclib import ezfuc
import json
import re


import manager
class Spider(manager.Spider):
    name = 'X--9'
    filter_data = True
    post_data = {
        "companyType": "%u65BD%u5DE5",
        "projectType": "%u623F%u5EFA",
        "keyWord": "",
        "EvalDate": str(time.strftime("%F")),
        "orderby": "PM",
        "oderType": "%u4ECA%u65E5%u6392%u540D",
        "startRange": "-1",
        "endRange": "-1",
        "startScore": "-1",
        "endScore": "-1",
        "pageIndex": "10",
        "pageSize": "10",
        "token": "",
        "opt": "0"
    }
    post_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Host": "http://pt.cdzj.chengdu.gov.cn:8024",
        # "Referer": "http://pt.cdzj.chengdu.gov.cn:8024/Integrity/ComprehensiveOrder/ConstructCompanOrder.aspx?DeftType=sgsz",
        "Connection": "keep-alive"
    }
    type_dict = {
        "X--9":"sgfjCertType",
        "X--8":"sgszCertType"
    }
    projectType = "%u623F%u5EFA"

    def start_requests(self):
        self.post_headers['User-Agent'] = ezfuc.random_ua()
        self.post_data['pageIndex'] = "1"
        self.post_data['projectType'] = self.projectType
        url = "http://pt.cdzj.chengdu.gov.cn:8024/Service/CreditRankWebSvr.assx/SearchComprehensiveCreditRankList"
        yield scrapy.FormRequest(
            url=url,
            headers=self.post_headers,
            meta={
                "pageIndex": 1,
            },
            formdata=self.post_data,
            dont_filter=True,
        )

    def parse(self, response):
        items = json.loads(json.loads(response.text)["Data"])['_Items']
        for i in items:
            url = f"http://pt.cdzj.chengdu.gov.cn:8024/Integrity/Construct/RankDetail.aspx?guid={i['Guid']}&companyType={i['CompanyType']}&CompanyGuid={i['CompanyGuid']}&projectType={i['ProjectType']}&VisiableTime={i['VisiableTime']}"
            item = CreditItem()
            item['企业名称'] = i['CompanyName']
            item['评价机构'] = "成都市建筑市场信用信息公示平台"
            item['今日得分'] = i['TotalScore']
            item['今日排名'] = i['RankIndex']
            item['六十日得分'] = i['AverageScore']
            item['六十日排名'] = i['AverageIndex']
            item['网站维护代码'] = self.name
            item['发布日期'] = re.search(r"(\S+)T", i['VisiableTime']).group(1)
            item['省'] = "四川"
            item['市'] = "成都"
            item['网站名称'] = "成都市建筑市场信用信息管理系统公示平台"
            item['url'] = url
            item['md5'] = ezfuc.md5([item['企业名称'], item['发布日期'], item['今日得分'], item['今日排名'], item['六十日得分'], item['六十日排名'], time.strftime("%F")+'-'])
            yield item

        TotalCount = json.loads(json.loads(response.text)["Data"])['TotalCount']
        if int(TotalCount) % 10 == 0:
            allPage = int(TotalCount) // 10
        else:
            allPage = int(TotalCount) // 10+1
        pageIndex = response.meta['pageIndex']
        if pageIndex < allPage:
            pageIndex += 1
            self.post_headers['User-Agent'] = ezfuc.random_ua()
            self.post_data['pageIndex'] = str(pageIndex)
            self.post_data['projectType'] = self.projectType
            yield scrapy.FormRequest(
                url=response.url,
                headers=self.post_headers,
                meta={
                     "pageIndex": pageIndex,
                 },
                formdata=self.post_data,
                dont_filter=True,
            )


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--9', 'auto', 1])