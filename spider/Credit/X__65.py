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
class X65Spider(manager.Spider):
    name = 'X--65'
    download_delay = float(gConfig.sleep_time)

    def __init__(self, *args, **kwargs):
        super(X65Spider, self).__init__(*args, **kwargs)
        # self.start_urls = ["http://cx.gzgreen.com/GZCXPT/GZCX_RankWebService.asmx/GetRankListSG"]
        self.post_header = {'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'zh-CN,zh;q=0.9',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Host': 'cx.gzgreen.com',
                            'Origin': 'http://cx.gzgreen.com',
                            'Referer': 'http://cx.gzgreen.com/GZCXPT/Screen/UFLAT/UserLogin.aspx',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                          '(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
                            'X-Requested-With': 'XMLHttpRequest'}
        self.post_data = {'dir': 'ASC',
                          'pageSize': '50',
                          'queryDate': format_time().y_m_d,
                          'sort': 'pm',
                          'startPos': '1',
                          'strEnterpriseName': ''}

    def start_requests(self):
        url = "http://cx.gzgreen.com/GZCXPT/GZCX_RankWebService.asmx/GetRankListSG"
        yield scrapy.FormRequest(
            url=url,
            dont_filter=True,
            callback=self.parse,
            headers=self.post_header,
            formdata=self.post_data
        )

    def parse(self, response):
        _, res = eamonn.ex(response.text, "xpath")
        totals = res.xpath("//rankresponse/recordtotalcount/text()")[0]
        total_pages = eamonn.page(totals, 50)
        for page in range(total_pages):
            self.post_data['startPos'] = str(1 + page * 50)
            yield scrapy.FormRequest(
                url="http://cx.gzgreen.com/GZCXPT/GZCX_RankWebService.asmx/GetRankListSG",
                dont_filter=True,
                callback=self.deal_parse,
                headers=self.post_header,
                formdata=self.post_data
            )

    def deal_parse(self, response):
        _, res = eamonn.ex(response.text, "xpath")
        trs = res.xpath("//rankdata")
        for tr in trs:
            # print(tr.xpath('./caluatedate/text()')[0])
            item_loader = CreditItem()
            item_loader['企业名称'] = tr.xpath('./enterprisename/text()')[0]
            item_loader['评价机构'] = "广州市园林绿化企业诚信综合评价体系信息平台"
            item_loader['行业'] = ""
            item_loader['专业'] = ""
            item_loader['信用得分'] = ""
            item_loader['信用等级'] = ""
            item_loader['排名'] = ""
            item_loader['今日得分'] = tr.xpath('./score/text()')[0]
            item_loader['今日排名'] = tr.xpath('./pm/text()')[0]
            item_loader['六十日得分'] = ""
            item_loader['六十日排名'] = ""
            item_loader['评价年度'] = ""
            item_loader['网站维护代码'] = "X--65"
            item_loader['发布日期'] = tr.xpath('./caluatedate/text()')[0]
            # item_loader['发布日期'] = eamonn.time(2)
            # item_loader['发布日期']=tr.ComputeDate
            item_loader['有效期'] = ""
            item_loader['省'] = "广东"
            item_loader['市'] = "广州"
            item_loader['网站名称'] = "广州市园林绿化企业诚信综合评价体系信息平台"
            item_loader[
                'url'] = f"http://cx.gzgreen.com/GZCXPT/CX/QYSFDA.aspx?qynm={tr.xpath('./enterpriseoid/text()')[0]}"

            yield item_loader
            # print(item_loader)


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--65', 'auto', 1])
