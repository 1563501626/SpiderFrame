# -*- coding: utf-8 -*-
import scrapy
import json
import time,hashlib,random


import manager
class Spider(manager.Spider):
    name = 'quanguogljs'
    allowed_domains = ['https://glxy.mot.gov.cn']
    # start_urls = ['https://glxy.mot.gov.cn/evaluate/index.do']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
            'XinYongpj_Spider.middlewares.ProxyMiddleware': 100,
            'XinYongpj_Spider.middlewares.TestDownloaderMiddleware': 101,

        },
        "ITEM_PIPELINES": {
            "XinYongpj_Spider.pipelines.TuniuPipeline": 300,
            # "XinYongpj_Spider.pipelines.ServerPipeline": 301
        }
    }
    post_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "glxy.mot.gov.cn",
        "Referer": "https://glxy.mot.gov.cn/evaluate/index.do",
        "Connection": "keep-alive"
    }
    post_data = {
        "page": "1",
        "rows": "15",
        "type": "0",
        "name": "",
        "oeriodCode": "",
        "evaGrade": "",
        "provinceCode": ""
    }
    type_list = ["0","2"]

    def start_requests(self):
        for i in self.type_list:
            self.post_data['type'] = i
            self.post_data['page'] = "1"
            self.post_headers['User-Agent'] = random.choice(mao_demo_tools.ua_list)
            url = "https://glxy.mot.gov.cn/evaluate/getEvaluateList.do"
            yield scrapy.FormRequest(
                url=url,
                headers=self.post_headers,
                meta={
                    "type":i,
                    "pageCount":1
                },
                formdata=self.post_data,
                dont_filter=True,
            )

    def parse(self, response):
        rows = json.loads(response.text)['rows']
        for row in rows:
            企业名称 = row['corpName']
            评价机构 = "全国公路建设市场信用信息管理系统"
            行业 = ""
            专业 = row['companyType']
            信用得分 = str(row['doScore'])
            信用等级 = row['evaGrade']
            排名 = ""
            今日得分 = ""
            今日排名 = ""
            六十得分 = ""
            六十日排名 = ""
            评价年度 = row['oeriodCode']
            网站维护代码 = "X--4"
            发布日期 = ""
            有效期 = ""
            省 = "国家"
            市 = "国家"
            网站名称 = "全国公路建设市场信用信息管理系统"
            url = response.url
            encode_md5 = mao_demo_tools.Md5(网站名称 + 企业名称 + 信用等级 + 发布日期 + url)
            item = XingYong()
            item['企业名称'] = 企业名称
            item['评价机构'] = 评价机构
            item['行业'] = 行业
            item['专业'] = 专业
            item['信用得分'] = 信用得分
            item['信用等级'] = 信用等级
            item['排名'] = 排名
            item['今日得分'] = 今日得分
            item['今日排名'] = 今日排名
            item['六十得分'] = 六十得分
            item['六十日排名'] = 六十日排名
            item['评价年度'] = 评价年度
            item['网站维护代码'] = 网站维护代码
            item['发布日期'] = 发布日期
            item['有效期'] = 有效期
            item['省'] = 省
            item['市'] = 市
            item['网站名称'] = 网站名称
            item['url'] = url
            item['data_time'] = time.strftime("%F")
            item['encode_md5'] = encode_md5
            item['update_code'] = "0"
            yield item
        maxPage = json.loads(response.text)['pageObj']['maxPage']
        pageCount = response.meta['pageCount']
        if pageCount<int(maxPage):
            pageCount +=1
            self.post_headers['User-Agent'] = random.choice(mao_demo_tools.ua_list)
            self.post_data['type'] = response.meta['type']
            self.post_data['page'] = str(pageCount)
            yield scrapy.FormRequest(
                url=response.url,
                headers=self.post_headers,
                meta={
                    "type": response.meta['type'],
                    "pageCount": pageCount
                },
                formdata=self.post_data,
                dont_filter=True,
            )




