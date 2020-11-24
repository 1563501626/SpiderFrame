# -*- coding: utf-8 -*-
import scrapy
import re

import random,time

import manager


class CdjxSpider(manager.Spider):
    name = 'cdjx'
    allowed_domains = ['http://pt.cdcin.com']
    start_urls = [
        'http://pt.cdcin.com/qyxx/qyxx_sgqy.do?flmbh=66&flmmc=WoZ9gRd5LaF1RQnYeqm56A&lmbh=105&lmmc=lXShHMyZpriJdC59ZM3nyA&curPage=-1',
        "http://pt.cdcin.com/qyxx/qyxx_kcsj.do?flmbh=66&flmmc=WoZ9gRd5LaF1RQnYeqm56A&lmbh=106&lmmc=WuxXBqGZR23Co8SSQ6Hgug&curPage=-1"
    ]
    # custom_settings = {
    #     # "ITEM_PIPELINES": {
    #     #     # "XinYongpj_Spider.pipelines.TuniuPipeline": 300,
    #     #     "XinYongpj_Spider.pipelines.ServerPipeline": 301
    #     # },
    #     "DOWNLOADER_MIDDLEWARES": {
    #         "XinYongpj_Spider.middlewares.ProcessAllExceptionMiddleware": 543
    #     }
    # }
    get_headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Host":"pt.cdcin.com",
        "Accept-Encoding":"gzip, deflate",
        "Connection":"keep-alive"
    }

    def parse(self, response):
        if "sgqy" in response.url:
            网站维护代码="X--19"

        else:
            网站维护代码 = "X--20"
        url_ = re.findall('location\.replace\("(.+?)"\+ page', response.text, re.S)[0]
        pageCount = re.search("pageCount=(\d+)&", url_).group(1)
        for i in range(1, int(pageCount) + 1):
            self.get_headers['User-Agent'] = random.choice(mao_demo_tools.ua_list)
            url = url_ + str(i)
            yield scrapy.Request(
                url=url,
                meta={
                    "网站维护代码":网站维护代码
                },
                headers=self.get_headers,
                dont_filter=True,
                callback=self.get_sgdata
            )



    def get_sgdata(self, response):
        tr_list = response.xpath('//table[@class="table-style1"]/tr[position()>1]')
        for item in tr_list:
            企业名称 = item.xpath('td/@title').extract_first('')
            评价机构 = "成都建信企业信息"
            行业 = ""
            专业 = ""
            信用得分 = ""
            信用等级 = ""
            排名 = ""
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = ""
            网站维护代码 = response.meta['网站维护代码']
            发布日期 = ''
            有效期 = ""
            省 = "四川"
            市 = "成都"
            网站名称 = "成都建信"
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


if __name__ == '__main__':
    import os
    os.system("scrapy crawl cdjx")

