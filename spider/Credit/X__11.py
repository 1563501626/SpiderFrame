# -*- coding: utf-8 -*-
import scrapy
from spider_code.confs import getConfig
from spider_code.items import CreditItem
import requests
from fuclib import ezfuc
from parsel import Selector
import re
import time

# configuration item
gConfig = getConfig.get_config()


import manager
class Spider(manager.Spider):
    name = 'X--11'
    filter_data = True
    filter_db = 'duplicate_key'
    filter_table = 'credit_x__11'
    start_urls = [
        'http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2']
    download_delay = 1.0
    page = 1
    first_data = {'ScriptManager1': 'ScriptManager1|btnLook', '__EVENTTARGET': '', '__EVENTARGUMENT': '',
                  '__VIEWSTATE': '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',
                  '__EVENTVALIDATION': 'on1JnMD0AZKp/5iy9kMDe+7Hst2mMWFPDHcB8uxlHyCHZmkGyS+kjucUuog3CQcctsm11o0cB5/NGB0KRJ18UA==',
                  'txt_lb': 'sg_sz', 'txt_key': '', 'AspNetPager_XWList_input': '1', 'AspNetPager_XWList2_input': '1',
                  'AspNetPager_XWList3_input': '1', 'AspNetPager_XWList4_input': '1', '__ASYNCPOST': 'true'}
    data = {'ScriptManager1': 'UpdatePanel4|AspNetPager_XWList2', 'txt_lb': 'sg_sz', 'txt_key': '',
            'AspNetPager_XWList_input': '1', 'AspNetPager_XWList2_input': '1', 'AspNetPager_XWList3_input': '1',
            'AspNetPager_XWList4_input': '1',
            '__VIEWSTATE': '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',
            '__EVENTTARGET': 'AspNetPager_XWList2', '__EVENTARGUMENT': '2',
            '__EVENTVALIDATION': 'WheTDB3slbVK6iKX30/o7GMPVAY8cKMGczi7U8+mmX7KMib4sjDx8Q17YTgjHi3mSk+9ZaWMRq3GBcLJYNWuww==',
            '__ASYNCPOST': 'true'}
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Host': 'cbs.chengdu.com.cn',
               'Origin': 'http://cbs.chengdu.com.cn', 'Referer': 'http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
               'X-MicrosoftAjax': 'Delta=true', 'X-Requested-With': 'XMLHttpRequest'}
    total = page + 1

    def parse(self, response):
        url = "http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2"
        self.first_data['__VIEWSTATE'] = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
        self.first_data['__EVENTVALIDATION'] = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
        yield scrapy.FormRequest(
            url=url,
            formdata=self.first_data,
            dont_filter=True,
            callback=self.parse_detail,
            meta={'page': self.page},
            headers=self.headers
        )

    def parse_detail(self, response):
        url = "http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2"
        self.data['__VIEWSTATE'] = re.search(r"__VIEWSTATE\|(.*?)\|", response.text).group(1)
        self.data['__EVENTVALIDATION'] = re.search(r"__EVENTVALIDATION\|(.*?)\|", response.text).group(1)
        self.data['__EVENTARGUMENT'] = str(self.page)
        if self.page <= self.total:
            yield scrapy.FormRequest(
                    url=url,
                    formdata=self.data,
                    dont_filter=True,
                    callback=self.parse_detail,
                    meta={'page': self.page},
                    headers=self.headers
                )
            current_page = response.xpath("//div[@id='AspNetPager_XWList2']//span/text()").extract_first()
            if (self.page == 1 and response.xpath("//a[not(@href)]/../../div[@class='cell cell_2']/..")) or \
                    (current_page and int(current_page) != 1):
                endpage = response.xpath("//div[@id='AspNetPager_XWList2']//a[text()='尾页']/@href").extract_first()
                self.total = int(endpage.split(",")[-1].split("'")[1])
                self.page += 1
                item = CreditItem()
                lis = response.xpath("//a[not(@href)]/../../div[@class='cell cell_2']/..")
                for i in lis:
                    item["企业名称"] = i.xpath("./div[1]/a/text()").extract_first().strip()
                    item["排名"] = i.xpath("./div[3]/text()").extract_first().strip()
                    item["今日得分"] = i.xpath("./div[4]/text()").extract_first().strip()
                    item["六十日得分"] = i.xpath("./div[5]/text()").extract_first().strip()
                    item["网站维护代码"] = self.name
                    item["省"] = "四川"
                    item["市"] = "成都"
                    item["网站名称"] = "成都市工程建设招标投标从业单位信用信息平台"
                    item['url'] = "http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2"
                    today = time.strftime("%F")
                    item['md5'] = ezfuc.md5(item["企业名称"], item["排名"], item["今日得分"], item["六十日得分"], today)
                    yield item
                    # print(item)


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--11', 'w', 1])
