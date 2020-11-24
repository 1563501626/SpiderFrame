# -*- coding: utf-8 -*-
import scrapy
import re
import time

from fuclib import ezfuc

from spider_code.items import AutoItem

city_value = {
    "320100": "南京市",
    "320200": "无锡市",
    "320300": "徐州市",
    "320400": "常州市",
    "320500": "苏州市",
    "320600": "南通市",
    "320700": "连云港市",
    "320800": "淮安市",
    "320900": "盐城市",
    "321000": "扬州市",
    "321100": "镇江市",
    "321200": "泰州市",
    "321300": "宿迁市"
}
import manager
class X33Spider(manager.Spider):
    name = 'X--33'
    # filter_data = True
    allowed_domains = ['http://58.213.147.230:7001']
    start_urls = [
        'http://58.213.147.230:7001/Jsjzyxyglpt/faces/public/creditEval.jsp?evaluationArea=320100&menucode=07']
    post_data = {
        "form:page": "1",
        "form:refreshAct": "",
        "form:city": "",
        "pageSize": "30",
        "com.sun.faces.VIEW": "",
        "form": "form"
    }

    def __init__(self, *args, **kwargs):
        super(X33Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        for c in city_value:
            url = "http://58.213.147.230:7001/Jsjzyxyglpt/faces/public/creditEval.jsp"
            view = response.xpath('//input[@name="com.sun.faces.VIEW"]/@value').extract_first('')
            self.post_data['com.sun.faces.VIEW'] = view
            self.post_data['form:city'] = c
            self.post_data['form:page'] = '1'
            yield scrapy.FormRequest(
                url=url,
                formdata=self.post_data,
                meta={"city": c,"pageNo":1},
                dont_filter=True,
                callback=self.ListData
            )

    def ListData(self, response):
        city = response.meta['city']
        items = response.xpath('//div/div[3]/table/tr')
        for it in items:
            for i in range(2, 7, 4):
                企业名称 = it.xpath(f'td[{i}]/div/@title').extract_first('')
                if 企业名称:
                    评价机构 = "江苏省建筑市场监管与诚信信息一体化平台"
                    行业 = ""
                    专业 = ""
                    信用得分 = it.xpath(f'td[{i+2}]/div/@title').extract_first('')
                    信用等级 = ""
                    排名 = ''
                    今日得分 = ''
                    今日排名 = ''
                    六十得分 = ''
                    六十日排名 = ''
                    评价年度 = ''
                    网站维护代码 = 'X--33'
                    发布日期 = it.xpath(f'td[{i+1}]/div/@title').extract_first('')
                    有效期 = ""
                    省 = "江苏"
                    市 = city_value[city]
                    网站名称 = "江苏省建筑市场监管与诚信信息一体化平台"
                    encode_md5 = ezfuc.md5(网站名称 + 企业名称 + 信用等级 + 发布日期 + response.url)
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
                    # item['md5'] = encode_md5
                    yield item
        pageNo = response.meta['pageNo']
        page_num = re.findall("页/共<b>(.+?)</b>页", response.text, re.S)
        # if not page_num:
        #     print(response.text)
        #     print(city)
        #     print(pageNo)
        if pageNo < int(page_num[0].strip()):
            pageNo+=1
            view = response.xpath('//input[@name="com.sun.faces.VIEW"]/@value').extract_first('')
            self.post_data['com.sun.faces.VIEW'] = view
            self.post_data['form:city'] = city
            self.post_data['form:page'] = str(pageNo)
            yield scrapy.FormRequest(
                url=response.url,
                formdata=self.post_data,
                meta={"city": city, "pageNo": pageNo},
                dont_filter=True,
                callback=self.ListData
            )


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--33', 'auto', 1])
