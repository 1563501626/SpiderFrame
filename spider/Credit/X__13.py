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
    name = 'X--13'
    start_urls = [
        'http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2']
    download_delay = 1.0
    page = 1
    filter_data = True
    filter_db = 'duplicate_key'
    filter_table = 'credit_x__13'
    first_data = {'ScriptManager1': 'ScriptManager1|btnLook', '__EVENTTARGET': '', '__EVENTARGUMENT': '',
                  '__VIEWSTATE': 'Xn4kpd1d5ZnstyBiHza86lTed+LFal11/jG89MkukXRAtytdib10rmZSi2UPqqQc',
                  '__EVENTVALIDATION': 'K4uMgDtjzL4o3TQu/QHkUPGqvTxf1LpWs8lG3cJgMxWDLSAb2YKBO0WEsvL++pg5rzSaX962ldOswRLrjKmlRQ==',
                  'txt_lb': '1', 'txt_key': '', 'AspNetPager_XWList_input': '1', 'AspNetPager_XWList2_input': '1',
                  'AspNetPager_XWList3_input': '1', 'AspNetPager_XWList4_input': '1', '__ASYNCPOST': 'true',
                  'btnLook': ''}
    data = {'ScriptManager1': 'UpdatePanel8|AspNetPager_XWList4', 'txt_lb': '1', 'txt_key': '',
            'AspNetPager_XWList_input': '1', 'AspNetPager_XWList2_input': '1', 'AspNetPager_XWList3_input': '1',
            'AspNetPager_XWList4_input': '1',
            '__VIEWSTATE': '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',
            '__EVENTTARGET': 'AspNetPager_XWList4', '__EVENTARGUMENT': '2',
            '__EVENTVALIDATION': 'xGsq0Ms1z65hH3JZvByifRx6Ffj2civa2nEs/JR9ZVdFy8lzo44+GtkU9kXB9NT3bt/3KXoyBWQzdGKXPuNaRQ==',
            '__ASYNCPOST': 'true'}
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'cbs.chengdu.com.cn',
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
            current_page = response.xpath("//div[@id='AspNetPager_XWList4']//span/text()").extract_first()
            if (self.page == 1 and response.xpath("//div[@id='AspNetPager_XWList3']/following-sibling::li")) or \
                    (current_page and int(current_page) != 1):
                self.page += 1
                lis = response.xpath("//div[@id='AspNetPager_XWList3']/following-sibling::li")
                for i in lis:
                    item = CreditItem()
                    item["企业名称"] = i.xpath("./div[1]/a/text()").extract_first().strip()
                    item["专业"] = i.xpath("./div[2]/text()").extract_first().strip()
                    item["排名"] = i.xpath("./div[3]/text()").extract_first().strip()
                    item["今日得分"] = i.xpath("./div[4]/text()").extract_first().strip()
                    item["六十日得分"] = i.xpath("./div[5]/text()").extract_first().strip()
                    item["网站维护代码"] = self.name
                    item["省"] = "四川"
                    item["市"] = "成都"
                    item["网站名称"] = "成都市工程建设招标投标从业单位信用信息平台"
                    item['url'] = self.start_urls[0]
                    today = time.strftime("%F")
                    item['md5'] = ezfuc.md5(item["企业名称"], item["排名"], item["今日得分"], item["六十日得分"], today)
                    yield item
                    # print(item)


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--13', 'auto', 1])
