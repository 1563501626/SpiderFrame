# -*- coding: utf-8 -*-
import scrapy
from spider_code.confs import getConfig
from spider_code.items import CreditItem
import re
import time
from fuclib import ezfuc

# configuration item
gConfig = getConfig.get_config()


import manager
class Spider(manager.Spider):
    name = 'X--18'
    start_urls = [
        'http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2']
    download_delay = 1.0
    page = 1
    filter_data = True
    filter_db = 'duplicate_key'
    filter_table = 'credit_x__18'
    first_data = {'ScriptManager1': 'ScriptManager1|btnLook', 'txt_lb': '7', 'txt_key': '',
                  'AspNetPager_XWList_input': '1', 'AspNetPager_XWList2_input': '1', 'AspNetPager_XWList3_input': '1',
                  'AspNetPager_XWList4_input': '1',
                  '__VIEWSTATE': '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',
                  '__EVENTTARGET': '', '__EVENTARGUMENT': '',
                  '__EVENTVALIDATION': 'ksWUR7A2kANY9vrUVQR3wJYBv4fVaHE/aof7bkoeaO8ZpvI8/x6N8fHsk+//WUcql/RmgY46umCngq55Rk5YKA==',
                  '__ASYNCPOST': 'true', 'btnLook': ''}
    data = {'ScriptManager1': 'UpdatePanel6|AspNetPager_XWList3', 'txt_lb': '7', 'txt_key': '',
            'AspNetPager_XWList_input': '1', 'AspNetPager_XWList2_input': '1', 'AspNetPager_XWList3_input': '1',
            'AspNetPager_XWList4_input': '1',
            '__VIEWSTATE': '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',
            '__EVENTTARGET': 'AspNetPager_XWList3', '__EVENTARGUMENT': '2',
            '__EVENTVALIDATION': 'ksWUR7A2kANY9vrUVQR3wJYBv4fVaHE/aof7bkoeaO8ZpvI8/x6N8fHsk+//WUcql/RmgY46umCngq55Rk5YKA==',
            '__ASYNCPOST': 'true'}
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Host': 'cbs.chengdu.com.cn',
               'Origin': 'http://cbs.chengdu.com.cn', 'Referer': 'http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
               'X-MicrosoftAjax': 'Delta=true', 'X-Requested-With': 'XMLHttpRequest'}
    total = 0

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
        endpage = response.xpath("//a[text()='尾页']/@href").extract_first()
        if not self.total:
            self.total = int(endpage.split(",")[-1].split("'")[1])
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
            current_page = response.xpath("//div[@id='AspNetPager_XWList3']//span/text()").extract_first()
            if (self.page == 1 and response.xpath("//div[@id='AspNetPager_XWList2']/following-sibling::li")) or \
                    (current_page and int(current_page) != 1):
                self.page += 1
                lis = response.xpath("//div[@id='AspNetPager_XWList2']/following-sibling::li")
                for i in lis:
                    item = CreditItem()
                    item["企业名称"] = i.xpath("./div[1]/a/@title").extract_first().strip()
                    item["专业"] = i.xpath("./div[2]/text()").extract_first().strip()
                    item["信用得分"] = i.xpath("./div[3]/text()").extract_first().strip()
                    item["信用等级"] = i.xpath("./div[4]/text()").extract_first().strip()
                    item["网站维护代码"] = self.name
                    item["省"] = "四川"
                    item["市"] = "成都"
                    item["网站名称"] = "成都市工程建设招标投标从业单位信用信息平台"
                    item['url'] = "http://cbs.chengdu.com.cn/Web/" + i.xpath("./div[1]/a/@href").extract_first().strip()
                    today = time.strftime("%F")
                    item['md5'] = ezfuc.md5(item["企业名称"], item["专业"], item["信用得分"], item["信用等级"], today)
                    yield item
                    # print(item)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--18'.split())
