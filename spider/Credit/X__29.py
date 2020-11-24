# -*- coding: utf-8 -*-
import scrapy
import json
import time

from spider_code.items import AutoItem


import manager
class Spider(manager.Spider):
    name = 'X--29'
    allowed_domains = ['http://61.190.26.79:5000']
    start_urls = ['http://61.190.26.79:5000/General/alljudge_json?page=1&limit=20&jtype=5&chnm=&apti=&result=&st=0']
    pn = 1
    z_d = {
        5: "施工",
        6: "监理"
    }

    def parse(self, response):
        items = json.loads(response.text)['data']
        for it in items:
            企业名称 = it['UNITNAME']
            评价机构 = "安徽省水利建设市场信用信息平台"
            行业 = ""
            专业 = self.z_d[it['JINDEX']]
            信用得分 = it['SCORE']
            信用等级 = it['RESULT']
            排名 = ''
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = ''
            网站维护代码 = 'X--29'
            发布日期 = ''
            有效期 = ""
            省 = "安徽"
            市 = "安徽"
            网站名称 = "安徽省水利建设市场信用信息平台"
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
        totalPage = json.loads(response.text)['totalPage']
        if self.pn < totalPage:
            self.pn += 1
            url = f"http://61.190.26.79:5000/General/alljudge_json?page={self.pn}&limit=20&jtype=5&chnm=&apti=&result=&st=0"
            yield scrapy.Request(
                url,
                dont_filter=True
            )


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(["scrapy", 'crawl', 'X--29'])
