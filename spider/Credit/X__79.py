# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from spider_code.api import hj_tools as eamonn
from spider_code.confs import getConfig
from spider_code.items import AutoItem
gConfig = getConfig.get_config()


import manager
class X75Spider(manager.Spider):
    name = 'X--79'
    download_delay = float(gConfig.sleep_time)

    def __init__(self, *args, **kwargs):
        super(X75Spider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://218.13.13.70/forUI/Credit/showCreditList.aspx"]
        self.url = "http://218.13.13.70/forUI/Credit/showCreditList.aspx"
        self.data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '/wEPDwUKMTYxMTkzMzkyOA9kFgICAw9kFggCBw8QZBAVBQzorr7orqHljZXkvY0M5pa95bel5Y2V5L2NDOebkeeQhuWNleS9jQzor5Xpqozmo4DmtYsM6YCg5Lu35ZKo6K+iFQUHMjEwMjAwMAcyMTAyMDAxBzIxMDIwMDIHMjEwMjAwMwcyMTAyMDA4FCsDBWdnZ2dnFgFmZAIJDxAPFgYeDkRhdGFWYWx1ZUZpZWxkBQVEb2NJRB4NRGF0YVRleHRGaWVsZAUKUGVyaW9kQ29kZR4LXyFEYXRhQm91bmRnZBAVBgzlvZPliY3nrYnnuqcZMjAxOeW5tOiuvuiuoeWNleS9jeivhOS7txkyMDE45bm06K6+6K6h5Y2V5L2N6K+E5Lu3GTIwMTflubTorr7orqHljZXkvY3or4Tku7cZMjAxNuW5tOiuvuiuoeWNleS9jeivhOS7txkyMDE15bm06K6+6K6h5Y2V5L2N6K+E5Lu3FQYDY3VyJGM3ODIxZGZhLThkMDctNDBlZC05M2NkLThiMzk3ZjlhYWEzYiQxM2U0ZTJmOS1mNmI0LTRhZGYtYTg5My05Mzc1NjA4NDNmNTMkYjY0YmQ2MjEtZmI3YS00MjliLTgwYjMtYTZhZjkwZDAxMzc5JDhmOGFjYTM3LTg0YzctNGVhMy05ZjI0LWQyMmY0OTZiMTUwNyQ1MzIwYTI2ZC00ZjY3LTRkODItOGVlYS1iYTU2OThmNWNjODQUKwMGZ2dnZ2dnFgECAWQCCw8QDxYGHwAFB0dyYWRlTm8fAQUHR3JhZGVObx8CZ2QQFQYG5YWo6YOoAkFBAUEBQgFDAUQVBgACQUEBQQFCAUMBRBQrAwZnZ2dnZ2cWAWZkAhUPDxYCHglUb3RhbFJvd3MCF2QWBmYPDxYCHgdFbmFibGVkaGRkAgIPDxYCHwRoZGQCBA8QDxYCHwJnZGQWAWZkZCGrHZ2OEtCTC5AIXsD4ZMYXoWgWeUKL6KqX/s8ZN24V',
            '__VIEWSTATEGENERATOR': 'BC47BF51',
            'Login1$txtUserName': '',
            'Login1$txtPassword': '',
            'Login1$txtValidCode': '',
            'Login1$Digest': '',
            'Login1$UserID': '',
            'Login1$epassSN': '',
            'Login1$RandomData': 'rpeksgfcxklgxvtswkih',
            'ddlCorpType': '2102000',
            'ddlPeriod': 'cur',
            'ddlGrade': '',
            'txtCorpCode': '',
            'txtCorpName': '',
            'btnQuery': '查询',
            'SqlPager1$ToPage': '1',
        }
        self.total = 0
        self.page = 1

    def parse(self, response):
        if not self.total:
            self.total = int(eamonn.page(re.search(r"共.*?(\d+).*?条", response.text).group(1), 17))
        self.data['__VIEWSTATE'] = response.xpath("//input[@name='__VIEWSTATE']/@value").extract_first()
        self.data['__VIEWSTATEGENERATOR'] = response.xpath("//input[@name='__VIEWSTATEGENERATOR']/@value").extract_first()
        self.data['Login1$RandomData'] = response.xpath("//input[@name='Login1$RandomData']/@value").extract_first()
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.data,
            dont_filter=True,
            callback=self.parse_detail
        )

    def parse_detail(self, response):
        trs = response.xpath("//table[@id='datagrid']/tr")[1:]
        for tr in trs:
            item_loader = AutoItem()
            item_loader['组织机构代码'] = tr.xpath("string(./td[2])").extract_first("").strip()
            item_loader['企业名称'] = tr.xpath("string(./td[3])").extract_first("").strip()
            item_loader['企业类型'] = tr.xpath("string(./td[4])").extract_first("").strip()
            item_loader['信用等级'] = tr.xpath("string(./td[5])").extract_first("").strip()
            item_loader['年份'] = str(datetime.datetime.now().year)
            item_loader['评价机构'] = "佛山市公路建设市场信用信息管理系统"
            item_loader['网站维护代码'] = "x--79"
            item_loader['网站名称'] = "佛山市公路建设市场信用信息管理系统"
            item_loader['url'] = response.url

            yield item_loader

        self.data['__VIEWSTATE'] = response.xpath("//input[@name='__VIEWSTATE']/@value").extract_first()
        self.data['__VIEWSTATEGENERATOR'] = response.xpath(
            "//input[@name='__VIEWSTATEGENERATOR']/@value").extract_first()
        self.data['Login1$RandomData'] = response.xpath("//input[@name='Login1$RandomData']/@value").extract_first()
        self.data['__EVENTTARGET'] = "SqlPager1$ToPage"
        if 'btnQuery' in self.data.keys():
            self.data.pop('btnQuery')
        self.page += 1
        self.data['SqlPager1$ToPage'] = str(self.page)
        if self.page <= self.total:
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.data,
                dont_filter=True,
                callback=self.parse_detail
            )


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--79'.split())
