# -*- coding: utf-8 -*-
import scrapy, re
import time

from spider_code.items import AutoItem


import manager
class Spider(manager.Spider):
    name = 'X--24'
    allowed_domains = ['http://www.zjjxzj.com']
    start_urls = ['http://www.zjjxzj.com/xinyongchaxun.aspx']
    post_data = {
        "__EVENTTARGET": "ctl00$ContentPlaceHolder1$anp",
        "__LASTFOCUS": "",
        "ctl00$top1$txtkey": "请输入关键字！",
        "ctl00$ContentPlaceHolder1$Dr_dj": "0",
        "ctl00$ContentPlaceHolder1$txtCpName": "",
        "ctl00$foot1$ddlshengnei": "http://www.hzgczj.cn/index.asp",
        "ctl00$foot1$ddlshengwai": "http://www.gsgczj.com.cn/",
        "ctl00$foot1$ddlqita": "http://www.jiaxing.gov.cn/"
    }
    pageNo = 1

    def parse(self, response):
        # print(response.text)
        items = response.xpath('//table[1]/tr[position()>1]')
        for it in items:
            企业名称 = it.xpath('td[2]/a/text()').extract_first('').strip()
            评价机构 = "嘉兴市造价网信用评价"
            行业 = ""
            专业 = it.xpath('td[3]/text()').extract_first('').strip()
            信用得分 = ''
            信用等级 = it.xpath('td[4]/text()').extract_first('').strip()
            排名 = ''
            今日得分 = ''
            今日排名 = ''
            六十日得分 = ''
            六十日排名 = ''
            评价年度 = ''
            网站维护代码 = 'X--24'
            发布日期 = ''
            有效期 = ""
            省 = "浙江"
            市 = "嘉兴"
            网站名称 = "嘉兴工程造价管理"
            Url = response.urljoin(it.xpath('td[2]/a/@href').extract_first(''))
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
            item['url'] = Url
            # print(item)
            yield item
        page_num = re.findall("(\d+)", response.xpath('//td[@class="paginator"][1]/text()').extract_first(''))[1]
        if self.pageNo < int(page_num):
            __VIEWSTATE = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first('')
            __EVENTVALIDATION = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first('')
            self.post_data['ctl00$ContentPlaceHolder1$anp_input'] = str(self.pageNo)
            self.pageNo += 1
            self.post_data['__EVENTARGUMENT'] = str(self.pageNo)
            self.post_data['__VIEWSTATE'] = __VIEWSTATE
            self.post_data['__EVENTVALIDATION'] = __EVENTVALIDATION
            yield scrapy.FormRequest(
                url=response.url,
                formdata=self.post_data,
                dont_filter=True
            )


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--24', 'auto', 1])
