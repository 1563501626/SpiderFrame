# -*- coding: utf-8 -*-
import scrapy
import re
from spider_code.api import hj_tools as eamonn
from spider_code.confs import getConfig
from spider_code.items import CreditItem
from lxml.etree import tostring
from fuclib import format_time
import ssl

# configuration item
gConfig = getConfig.get_config()


import manager
class Spider(manager.Spider):
    name = 'X--70'
    download_delay = float(gConfig.sleep_time)
    ssl._create_default_https_context = ssl._create_unverified_context

    def __init__(self, pagecount=50, *args, **kwargs):
        super(X70Spider, self).__init__(*args, **kwargs)
        # self.start_urls = ["https://cxpt.fssjz.cn/cxpt/web/enterprise/getEnterpriseList.do"]
        self.post_header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'zh-CN,zh;q=0.9',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Host': 'cxpt.fssjz.cn',
                            'Origin': 'https://cxpt.fssjz.cn',
                            'Referer': 'https://cxpt.fssjz.cn/cxpt/website/enterpriseList.jsp',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                          '(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
                            'X-Requested-With': 'XMLHttpRequest'}
        self.post_data = {'aptText': '',
                          'areaCode': '0',
                          'entName': '',
                          'mainZZ': '0',
                          'pageIndex': '1',
                          'pageSize': '10'}
        self.get_page = pagecount

    def start_requests(self):
        url = "http://cxpt.fssjz.cn/cxpt/web/enterprise/getEnterpriseList.do"
        yield scrapy.FormRequest(
            url=url,
            dont_filter=True,
            callback=self.parse,
            headers=self.post_header,
            formdata=self.post_data
        )

    def parse(self, response):
        _, res = eamonn.ex(response.text, "json")
        total_pages = eamonn.page(res.total, 10)
        for page in range(total_pages):
            self.post_data['pageIndex'] = str(page)
            yield scrapy.FormRequest(
                url=response.url,
                dont_filter=True,
                callback=self.deal_parse,
                headers=self.post_header,
                formdata=self.post_data
            )

    def deal_parse(self, response):
        _, res = eamonn.ex(response.text, "json")
        trs = res.data
        for tr in trs:
            item_loader = CreditItem()
            item_loader['企业名称'] = tr['corpName']
            item_loader['评价机构'] = "佛山市建筑行业诚信管理平台"
            item_loader['行业'] = ""
            item_loader['专业'] = tr['typename']
            item_loader['信用得分'] = tr['mark']
            item_loader['信用等级'] = tr["dengji"]
            item_loader['排名'] = ""
            item_loader['今日得分'] = ""
            item_loader['今日排名'] = ""
            item_loader['六十日得分'] = ""
            item_loader['六十日排名'] = ""
            item_loader['评价年度'] = ""
            item_loader['网站维护代码'] = "X--70"
            item_loader['发布日期'] = ""
            item_loader['有效期'] = ""
            item_loader['省'] = "广东"
            item_loader['市'] = "佛山"
            item_loader['网站名称'] = "佛山市建筑诚信评价体系管理平台"
            item_loader[
                'url'] = f'https://cxpt.fssjz.cn/cxpt/website/enterpriseInfo.jsp?entID={tr["corpCode"]}&eid={tr["id"]}&bid={tr["bid"]}'

            yield item_loader
            # print(item_loader)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--70'.split())
