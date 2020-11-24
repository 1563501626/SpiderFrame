# -*- coding: utf-8 -*-
import re
import pandas as pd
import scrapy
from spider_code.api import hj_tools as eamonn
from spider_code.confs import getConfig
from spider_code.items import AutoItem
gConfig = getConfig.get_config()


import manager
class X75Spider(manager.Spider):
    name = 'X--78'
    download_delay = float(gConfig.sleep_time)

    def __init__(self, *args, **kwargs):
        super(X75Spider, self).__init__(*args, **kwargs)
        self.start_urls = ["https://jy.ggzy.foshan.gov.cn/TPBidder/HuiYuanInfoMis2_FS/Pages/JiaoTongChengXin/JiaoTongChengXin_List.aspx"]
        self.url = "https://jy.ggzy.foshan.gov.cn/TPBidder/HuiYuanInfoMis2_FS/Pages/JiaoTongChengXin/JiaoTongChengXin_List.aspx"
        self.data = {
            'ctl00$ScriptManager1': 'ctl00$UpdatePanel4|ctl00$cphContent$DataGrid1$ctl12',
            'ctl00$cphCondition$txtQYMC': '',
            'ctl00$cphCondition$txtCXBH': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_0': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_1': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_2': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_3': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_4': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_5': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_6': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_7': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_8': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_9': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_10': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_11': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_12': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_13': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_14': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_15': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_16': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_17': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_18': '',
            'ctl00_cphContent_DataGrid1_RowSelecter_19': '',
            'ctl00$cphContent$DataGrid1$PageNumDataGrid1': '3',
            '__EVENTTARGET': 'ctl00$cphContent$DataGrid1$ctl12',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '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',
            '__VIEWSTATEGENERATOR': 'C195EA74',
            '__EVENTVALIDATION': 'Ou9qCrAxd9zqpE7flSCLcxoPfaJ26PvxQgclretbMld1j+GjM2GuxGJAL8cZ5+RWUHUaI1BpogzvgA32PUA2eSpvCUvn2zQhcnGkdVTFObinHMIQ32BXB0/QzCBe8Vu5LXwPJtfIV9uci5DYDa76Gcz4ApK7/19PFNY2Z56paKcNbFoEzg+LRy4I5HK14zw0wFSkBAueUw50coH0ym2x2K4BsWxF/h2hU2+ExVehuca45PymTcvaf3uqeu7PpT6Jzz/ZoD6pfIfiF6Cxmh+QjGBHJImzKWAIbpQI/l5HDzOa7d/1wZJLJyaqfwbik42tz7i+HcAw2XSIw/etFcWk/ENeur0gY24vIZKWy2+WsSbH2U0rDj21kD1VSeo7YqznHgWudtMe0SaJONs2rLqDiWcyjKK4HCtOcAD9FTcFQYeVvAI/hhQnmKeuifYZT/G6TCf3Xmv6F4osF0i9pkH5dZRS0dCJvkZIloLuDQQF7IudBrJCPfN3bZ1j/RbM5okWbJqIlyBStv4XvUvi',
            'ctl00_cphContent_DataGrid1_ClientState': '{}',
            '__ASYNCPOST': 'true',
        }
        self.total = 0
        self.page = 1

    def parse(self, response):
        if not self.total:
            self.total = int(re.search(r"总页数：(\d+)", response.text).group(1))
        trs = response.xpath("//table[@id='DataGrid1_BodyTable']/tr")
        for tr in trs:
            item_loader = AutoItem()
            item_loader['企业名称'] = tr.xpath("string(./td[@colname='企业名称'])").extract_first("").strip()
            item_loader['企业类型'] = tr.xpath("string(./td[@colname='企业类型'])").extract_first("").strip()
            item_loader['诚信编号'] = tr.xpath("string(./td[@colname='诚信编号'])").extract_first("").strip()
            item_loader['信用等级'] = tr.xpath("string(./td[@colname='考评等级（诚信等级）'])").extract_first("").strip()
            item_loader['信用得分'] = tr.xpath("string(./td[@colname='诚信分值'])").extract_first("").strip()
            item_loader['企业状态'] = tr.xpath("string(./td[@colname='企业状态'])").extract_first("").strip()
            item_loader['评价机构'] = "佛山市城市道路诚信信息公示"
            item_loader['网站维护代码'] = "x--78"
            item_loader['网站名称'] = "佛山市公共资源交易中心"
            item_loader['url'] = response.url

            yield item_loader
        self.page += 1
        self.data['__VIEWSTATE'] = response.xpath("//input[@name='__VIEWSTATE']/@value").extract_first()
        self.data['__EVENTVALIDATION'] = response.xpath("//input[@name='__EVENTVALIDATION']/@value").extract_first()
        self.data['ctl00$cphContent$DataGrid1$PageNumDataGrid1'] = str(self.page)
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.data,
            dont_filter=True,
            callback=self.parse_detail
        )

    def parse_detail(self, response):
        trs = response.xpath("//table[@id='DataGrid1_BodyTable']/tr")
        for tr in trs:
            item_loader = AutoItem()
            item_loader['企业名称'] = tr.xpath("string(./td[@colname='企业名称'])").extract_first("").strip()
            item_loader['企业类型'] = tr.xpath("string(./td[@colname='企业类型'])").extract_first("").strip()
            item_loader['诚信编号'] = tr.xpath("string(./td[@colname='诚信编号'])").extract_first("").strip()
            item_loader['信用等级'] = tr.xpath("string(./td[@colname='考评等级（诚信等级）'])").extract_first("").strip()
            item_loader['信用得分'] = tr.xpath("string(./td[@colname='诚信分值'])").extract_first("").strip()
            item_loader['企业状态'] = tr.xpath("string(./td[@colname='企业状态'])").extract_first("").strip()
            item_loader['评价机构'] = "佛山市城市道路诚信信息公示"
            item_loader['网站维护代码'] = "x--78"
            item_loader['网站名称'] = "佛山市公共资源交易中心"
            item_loader['url'] = response.url

            yield item_loader

        self.data['__VIEWSTATE'] = re.search(r"__VIEWSTATE\|(.*?)\|", response.text).group(1)
        self.data['__EVENTVALIDATION'] = re.search(r"__EVENTVALIDATION\|(.*?)\|", response.text).group(1)
        self.data['__VIEWSTATEGENERATOR'] = re.search(r"__VIEWSTATEGENERATOR\|(.*?)\|", response.text).group(1)
        self.data['ctl00$cphContent$DataGrid1$PageNumDataGrid1'] = str(self.page)
        self.page += 1
        if self.page <= self.total:
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.data,
                dont_filter=True,
                callback=self.parse_detail
            )


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--78'.split())
