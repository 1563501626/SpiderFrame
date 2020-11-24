# -*- coding: utf-8 -*-
import scrapy
import re
from spider_code.api import hj_tools as eamonn
from spider_code.confs import getConfig
from spider_code.items import CreditItem
from fuclib import ezfuc

# configuration item
gConfig = getConfig.get_config()


import manager
class X72Spider(manager.Spider):
    name = 'X--72'
    download_delay = float(gConfig.sleep_time)

    def __init__(self, pagecount=50, *args, **kwargs):
        super(X72Spider, self).__init__(*args, **kwargs)
        # self.start_urls = ["http://210.76.74.108/xydtgl/xydtgl.showQyxytj.action"]
        self.post_header = ezfuc.struct_header("""POST /xydtgl/xydtgl.showQyxytj.action HTTP/1.1
                                        Host: 210.76.74.108
                                        Connection: keep-alive
                                        Accept: */*
                                        X-Requested-With: XMLHttpRequest
                                        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36
                                        Content-Type: application/x-www-form-urlencoded;utf-8
                                        Origin: http://210.76.74.108
                                        Referer: http://210.76.74.108/jsp/xyxxpt/qyxytj.jsp?lx=1
                                        Accept-Encoding: gzip, deflate
                                        Accept-Language: zh-CN,zh;q=0.9""")
        self.post_data = ezfuc.struct_data("page=1&count=20&qymc=&qylx=设计企业&szqy=")
        self.get_page = pagecount

    def start_requests(self):
        url = "http://210.76.74.108/xydtgl/xydtgl.showQyxytj.action"
        yield scrapy.FormRequest(
            url=url,
            dont_filter=True,
            callback=self.parse,
            headers=self.post_header,
            formdata=self.post_data
        )

    def parse(self, response):
        _, res = eamonn.ex(response.text, "json")
        total_pages = res.pageCount
        for page in range(1, int(total_pages) + 1):
            self.post_data['page'] = str(page)
            yield scrapy.FormRequest(
                url=response.url,
                dont_filter=True,
                callback=self.deal_parse,
                headers=self.post_header,
                formdata=self.post_data
            )

    def deal_parse(self, response):
        _, res = eamonn.ex(response.text, "json")
        trs = res.result
        for tr in trs:
            item_loader = CreditItem()
            item_loader['企业名称'] = tr["mc"]
            item_loader['评价机构'] = "广东省水利建设市场信用信息平台"
            item_loader['行业'] = ""
            item_loader['专业'] = ""
            item_loader['信用得分'] = tr["score"]
            item_loader['信用等级'] = ""
            item_loader['排名'] = ""
            item_loader['今日得分'] = ""
            item_loader['今日排名'] = ""
            item_loader['六十日得分'] = ""
            item_loader['六十日排名'] = ""
            item_loader['评价年度'] = ""
            item_loader['网站维护代码'] = "X--72"
            item_loader['发布日期'] = ""
            item_loader['有效期'] = ""
            item_loader['省'] = "广东"
            item_loader['市'] = "广东"
            item_loader['网站名称'] = "广东省水利建设市场信用信息平台"
            item_loader[
                'url'] = f'http://210.76.74.108/jsp/xyxxpt/xqlist.jsp?qyf=1&id={tr["id"]}'

            yield item_loader
            # print(item_loader)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--72'.split())
