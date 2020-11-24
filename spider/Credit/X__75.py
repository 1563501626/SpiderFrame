# -*- coding: utf-8 -*-
import scrapy
import re
from spider_code.api import hj_tools as eamonn
from spider_code.confs import getConfig
from spider_code.items import CreditItem
from lxml.etree import tostring
from fuclib import format_time

# configuration item
gConfig = getConfig.get_config()


import manager
class X75Spider(manager.Spider):
    name = 'X--75'
    download_delay = float(gConfig.sleep_time)

    def __init__(self, pagecount=50, *args, **kwargs):
        super(X75Spider, self).__init__(*args, **kwargs)
        # self.start_urls = ["http://219.131.222.107:9001/default.aspx?pageindex=1"]
        self.post_header = {}
        self.post_data = {}
        self.get_page = pagecount

    def start_requests(self):
        url = "http://219.131.222.107:9001/default.aspx?pageindex=1"
        yield scrapy.Request(
            url=url,
            dont_filter=True,
            callback=self.parse,
        )

    def parse(self, response):
        total_pages = response.css('a:contains("末页")::attr(href)').extract_first("")
        _, total_pages = eamonn.ex(total_pages, ['re', 'ndex=(.*)'])
        for page in range(1, int(total_pages) + 1):
            url = f"http://219.131.222.107:9001/default.aspx?pageindex={page}"
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                callback=self.deal_parse,
            )

    def deal_parse(self, response):
        trs = response.css('#FormUnit+table tr:nth-child(n+2)')
        for tr in trs:
            item_loader = CreditItem()
            item_loader['企业名称'] = tr.css('td:nth-child(2)>a::text').extract_first("")
            item_loader['评价机构'] = "珠海市市政和林业局企业信息管理平台"
            item_loader['行业'] = ""
            item_loader['专业'] = ""
            item_loader['信用得分'] = tr.css('td:nth-child(7)::text').extract_first("")
            item_loader['信用等级'] = tr.css('td:nth-child(8)::text').extract_first("")
            item_loader['排名'] = tr.css('td:nth-child(1)::text').extract_first("")
            item_loader['今日得分'] = ""
            item_loader['今日排名'] = ""
            item_loader['六十日得分'] = ""
            item_loader['六十日排名'] = ""
            item_loader['评价年度'] = ""
            item_loader['网站维护代码'] = "X--75"
            item_loader['发布日期'] = ""
            item_loader['有效期'] = ""
            item_loader['省'] = "广东"
            item_loader['市'] = "珠海"
            # item_loader['所在区域'] = ""
            item_loader['网站名称'] = "珠海市园林绿化企业信息管理平台"
            item_loader[
                'url'] = response.urljoin(tr.css('td:nth-child(2)>a::attr(href)').extract_first(""))

            yield item_loader
            # print(item_loader)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--75'.split())
