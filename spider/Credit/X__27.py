# -*- coding: utf-8 -*-
import scrapy
from math import ceil
import json, time
from spider_code.items import AutoItem
from fuclib import ezfuc


import manager
class Spider(manager.Spider):
    filter_data = True
    name = 'x--27'
    allowed_domains = ['http://61.190.70.122:8003']
    start_urls = ['http://http://61.190.70.122:8003/']
    post_data = {
        "pagesize": "12",
        "pageindex": "1",
        "txt": "",
        "type": "2",
        "CorpName": "",
        "CorpCode": "",
        "CorpType": "0"
    }

    def start_requests(self):
        url = "http://61.190.70.122:8003/epoint-mini/rest/function/searchXY"
        yield scrapy.FormRequest(
            url=url,
            meta={"pageNo": 1},
            formdata=self.post_data,
            dont_filter=True
        )

    def parse(self, response):
        items = json.loads(response.text)['all']['listinfo']
        for it in items:
            企业名称 = it['corpname']
            评价机构 = "安徽省住房和城乡建设项目信用得分"
            行业 = ""
            专业 = ''
            信用等级 = ''
            排名 = ''
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = ''
            发布日期 = ''
            有效期 = ""
            省 = "安徽"
            市 = "安徽"
            网站名称 = "安徽省住房和城乡建设厅"
            Url = f"http://dohurd.ah.gov.cn/ahzjt_front/searchpage/info_ser.html?type=5&corpcode={it['corpcode']}"
            encode_md5 = ezfuc.md5(网站名称 + 企业名称 + 信用等级 + 发布日期 + Url)

            item = AutoItem()
            item['企业名称'] = 企业名称
            item['评价机构'] = 评价机构
            item['行业'] = 行业
            item['专业'] = 专业
            item['信用得分'] = it['creditfjscore']
            item['信用等级'] = 信用等级
            item['排名'] = 排名
            item['今日得分'] = 今日得分
            item['今日排名'] = 今日排名
            item['六十日得分'] = 六十得分
            item['六十日排名'] = 六十日排名
            item['评价年度'] = 评价年度
            item['网站维护代码'] = "X--27"
            item['发布日期'] = 发布日期
            item['有效期'] = 有效期
            item['省'] = 省
            item['市'] = 市
            item['网站名称'] = 网站名称
            item['url'] = Url
            item['md5'] = encode_md5
            yield item

        pageNo = response.meta['pageNo']
        page_num = ceil(json.loads(response.text)['all']["total"] / 12)
        if pageNo < page_num:
            pageNo += 1
            self.post_data['pageindex'] = str(pageNo)
            yield scrapy.FormRequest(
                url=response.url,
                meta={"pageNo": pageNo},
                formdata=self.post_data,
                dont_filter=True
            )


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(["scrapy", 'crawl', 'x--27'])
