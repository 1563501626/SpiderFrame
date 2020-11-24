# -*- coding: utf-8 -*-
import scrapy
import re, time

from spider_code.items import AutoItem


import manager
class Spider(manager.Spider):
    name = 'X--63'
    allowed_domains = ['203.93.109.52:8088']
    start_urls = ['http://203.93.109.52:8088/']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
    }

    def start_requests(self):
        yield scrapy.Request(
            url='http://203.93.109.52:8088/gl/common/gl/corpinfo/scorelist',
            headers=self.headers,
            meta={"pageNo": 1},
            dont_filter=True
        )

    def parse(self, response):
        items = response.xpath('//table[@id="sample-table-1"]/tbody/tr')
        for it in items:
            企业名称 = it.xpath('td[2]/a/text()').extract_first('')
            评价机构 = "重庆市公路建设市场信用信息管理系统"
            行业 = ""
            专业 = it.xpath('td[4]/text()').extract_first('').strip()
            信用得分 = it.xpath('td[5]/a/text()').extract_first('')
            信用等级 = ''
            排名 = ''
            今日得分 = ''
            今日排名 = ''
            六十日得分 = ''
            六十日排名 = ''
            评价年度 = ''
            网站维护代码 = 'X--63'
            发布日期 = ''
            有效期 = ""
            省 = "重庆"
            市 = "重庆"
            网站名称 = "重庆市建筑企业诚信综合评价"
            url = response.urljoin(it.xpath('td[2]/a/@href').extract_first(''))
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
            item['六十日得分'] = 六十日得分
            item['六十日排名'] = 六十日排名
            item['评价年度'] = 评价年度
            item['网站维护代码'] = 网站维护代码
            item['发布日期'] = 发布日期
            item['有效期'] = 有效期
            item['省'] = 省
            item['市'] = 市
            item['网站名称'] = 网站名称
            item['url'] = url
            yield item

        page_num = \
        re.findall("条记录.*?/(.+?)页", response.xpath('//div[@id="sample_2_info"]/text()').extract_first(''), re.S)[0]
        pageNo = response.meta['pageNo']
        if pageNo < int(page_num):
            url = f"http://203.93.109.52:8088/gl/common/gl/corpinfo/scorelist?corp_Name=&corp_type=&city_area=&page={pageNo}&"
            pageNo += 1
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                meta={"pageNo": pageNo},
                dont_filter=True
            )


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--63', 'auto', 1])
