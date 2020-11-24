# -*- coding: utf-8 -*-
import datetime

import scrapy
import re
from spider_code.api import hj_tools as eamonn
from spider_code.confs import getConfig
from spider_code.items import CreditItem

gConfig = getConfig.get_config()


import manager
class X66Spider(manager.Spider):
    name = 'X--69'
    download_delay = float(gConfig.sleep_time)

    def __init__(self, pagecount=50, *args, **kwargs):
        super(X66Spider, self).__init__(*args, **kwargs)
        # self.start_urls = ["http://121.8.226.19/gzswcx/client/credit/EntSyntheticalCredit/getEntSyntheticalCredit.htm"]
        self.post_header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': '121.8.226.19',
            'Origin': 'http://121.8.226.19',
            'Referer': 'http://121.8.226.19/gzswcx/client/credit/EntSyntheticalCredit/getEntSyntheticalCredit.htm?fslx=102',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
        self.post_data = {'fslx': '204',
                          'page': '2',
                          'pageSize': '8',
                          'quarter': '10-01:12-31',
                          'qymc': '',
                          'year': '2019'}

        self.quarter = {'第一季度': '01-01:03-31', '第二季度': '04-01:06-30', '第三季度': '07-01:09-30', '第四季度': '10-01:12-31'}
        self.year = str(datetime.datetime.now().year)
        self.get_page = pagecount
        month = datetime.datetime.now().month
        self.jd_L = ''
        if 3 <= month < 6:
            self.jd_L = "第一季度"
        elif 6 <= month < 9:
            self.jd_L = "第二季度"
        elif 9 <= month < 12:
            self.jd_L = "第三季度"
        else:
            self.jd_L = "第四季度"

    def start_requests(self):
        year = self.year
        quarter = self.quarter[self.jd_L]
        self.post_data['year'] = year
        self.post_data['quarter'] = quarter
        url = "http://121.8.226.19/gzswcx/client/credit/Kcsj_qycxzhpj/getKcsj_qycxzhpj.htm"
        yield scrapy.FormRequest(
            url=url,
            dont_filter=True,
            callback=self.parse,
            headers=self.post_header,
            formdata=self.post_data,
            meta={'year': year}
        )

    def parse(self, response):
        total_pages = response.css('.last::attr(onclick)').extract_first("")
        _, res = eamonn.ex(total_pages, ["re", "', '(.*?)'\)"])
        if res:
            for page in range(1, int(res) + 1):
                self.post_data['page'] = str(page)
                self.post_data['year'] = response.meta['year']
                self.post_data['quarter'] = self.quarter[self.jd_L]
                yield scrapy.FormRequest(
                    url=response.url,
                    dont_filter=True,
                    callback=self.deal_parse,
                    headers=self.post_header,
                    formdata=self.post_data,
                    meta={'year': response.meta['year']}
                )

    def deal_parse(self, response):
        trs = response.css('.fenlei tr[height="40"]')
        for tr in trs:
            item_loader = CreditItem()
            item_loader['企业名称'] = tr.css('a::text').extract_first("")
            item_loader['评价机构'] = "广州市水务工程企业信息库及诚信管理"
            item_loader['行业'] = ""
            item_loader['专业'] = ""
            item_loader['信用得分'] = tr.css('td:nth-child(7)::text').extract_first("")
            item_loader['信用等级'] = ""
            item_loader['排名'] = tr.css('td:nth-child(3)::text').extract_first("")
            item_loader['今日得分'] = ""
            item_loader['今日排名'] = ""
            item_loader['六十日得分'] = ""
            item_loader['六十日排名'] = ""
            year = response.meta['year']
            self.post_data['year'] = response.meta['year']
            item_loader['评价年度'] = f"{year}，{self.jd_L}"
            item_loader['网站维护代码'] = "X--69"
            item_loader['发布日期'] = tr.css('td:nth-child(8)::text').extract_first("")
            item_loader['有效期'] = ""
            item_loader['省'] = "广东"
            item_loader['市'] = "广州"
            item_loader['网站名称'] = "广州市水务工程企业信息库及诚信中心"
            item_loader['url'] = response.urljoin(tr.css('a::attr(href)').extract_first(""))

            yield item_loader
            # print(item_loader)


if __name__ == '__main__':
    from manager import run

    run(['Credit', 'X--69', 'auto', 1])
