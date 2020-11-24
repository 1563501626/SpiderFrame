# -*- coding: utf-8 -*-
import requests
import scrapy
import re, datetime
import time

from parsel import Selector

from spider_code.items import AutoItem


import manager
class Spider(manager.Spider):
    name = 'X--60'
    allowed_domains = ['http://183.66.171.78:8011']
    start_urls = ['http://183.66.171.78:8011/CX_SGQYMRPM2.aspx']
    post_data = {
        "__EVENTTARGET": "GV_SGPM$ctl16$LinkButtonNextPage",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "txt_mc": "",
        "ddl_qylx": "",
        "txt_start": time.strftime("%F").replace("-", '/'),
    }
    total = 0

    def before_request(self, ret):
        if ret['meta'].get('flag', 0):
            res = requests.get(self.start_urls[0]).content.decode()
            response = Selector(res)
            self.post_data['__VIEWSTATE'] = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first('')
            self.post_data['__VIEWSTATEGENERATOR'] = response.xpath(
                '//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first('')
            self.post_data['__EVENTVALIDATION'] = response.xpath(
                '//input[@id="__EVENTVALIDATION"]/@value').extract_first('')
            self.post_data['GV_SGPM$ctl16$ddlPageGoto'] = str(ret['meta']['page'])
            ret['data'] = self.post_data
        return ret

    def parse(self, response):
        page = response.meta.get('page', 1)
        items = response.xpath("//table[@id='GV_SGPM']/tr[position()<last() and position()>1]")
        for item in items:
            企业名称 = item.xpath('td[3]/text()').extract_first('')
            评价机构 = "重庆市建筑企业诚信综合评价"
            行业 = ''
            专业 = ''
            信用得分 = ''
            信用等级 = ''
            排名 = ""
            今日得分 = item.xpath('td[8]/text()').extract_first('')
            今日排名 = item.xpath('td[2]/text()').extract_first('')
            六十日得分 = ''
            六十日排名 = ''
            评价年度 = ""
            网站维护代码 = "X--60"
            发布日期 = item.xpath('td[9]/text()').extract_first('')
            有效期 = ""
            省 = "重庆"
            市 = "重庆"
            网站名称 = "重庆市建筑企业诚信综合评价"
            dt = re.findall("javascript:OpenShow\('(.+?)','(.+?)'\)", item.xpath('td[10]/a/@href').extract_first(''))[0]
            url = f"http://183.66.171.78:8011/CX_QYCXDFXX.aspx?QYBM={dt[0]}&DATE={dt[1]}"
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
        if not self.total:
            self.total = int(re.search(r"共\s*(\d+)\s*页", response.text).group(1))
        if page < self.total:
            page += 1
            self.post_data['__VIEWSTATE'] = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first('')
            self.post_data['__VIEWSTATEGENERATOR'] = response.xpath(
                '//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first('')
            self.post_data['__EVENTVALIDATION'] = response.xpath(
                '//input[@id="__EVENTVALIDATION"]/@value').extract_first('')
            self.post_data['GV_SGPM$ctl16$ddlPageGoto'] = str(page)
            yield scrapy.FormRequest(
                url=response.url,
                formdata=self.post_data,
                dont_filter=True,
                meta={'page': page, 'flag': 1}
            )


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--60', 'auto', 1])
