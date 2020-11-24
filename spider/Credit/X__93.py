# -*- coding: utf-8 -*-
import datetime
import re
import time

import scrapy
from spider_code.confs import getConfig
from spider_code.items import AutoItem
from fuclib import format_time
from fuclib import ezfuc
import json

# configuration item
gConfig = getConfig.get_config()


import manager
class Spider(manager.Spider):
    name = 'X--93'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'hbjzxhcredit.org.cn:10005',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',}
    start_urls = ['http://hbjzxhcredit.org.cn:10005/credit/creditrating?like_companyName=&memberApplyModel.like_ZSBH=&memberApplyModel.equal_PJND=&memberApplyModel.equal_XYDJ=&p=2']
    url = 'http://hbjzxhcredit.org.cn:10005/credit/creditrating?like_companyName=&memberApplyModel.like_ZSBH=&memberApplyModel.equal_PJND=&memberApplyModel.equal_XYDJ=&p={page}'
    download_delay = float(gConfig.sleep_time)
    total = 0

    def parse(self, response):
        if not self.total:
            self.total = int(response.xpath("//a[text()='末页']/@href").extract_first().split("&p=")[-1])
        for i in range(1, self.total + 1):
            yield scrapy.Request(
                url=self.url.format(page=i),
                headers=self.headers,
                callback=self.deal_parse,
                dont_filter=True
            )

    def deal_parse(self, response):
        trs = response.xpath("//table[@class='ind-tab ind-tab-list']/tbody/tr[position()>1]")
        for tr in trs:
            item_loader = AutoItem()
            item_loader['企业名称'] = tr.xpath("./td[2]/a/text()").extract_first("").strip()
            item_loader['证书编号'] = tr.xpath("./td[3]/text()").extract_first("").strip()
            item_loader['评价年度'] = tr.xpath("./td[4]/text()").extract_first("").strip()
            item_loader['信用等级'] = tr.xpath("./td[5]/text()").extract_first("").strip()
            item_loader['发布日期'] = tr.xpath("./td[6]/text()").extract_first("").strip()
            item_loader['有效期'] = tr.xpath("./td[7]/text()").extract_first("").strip()
            item_loader['评价机构'] = "湖北省建筑施工企业信用体系建设平台"
            item_loader['网站维护代码'] = "X--93"
            item_loader['省'] = "湖北"
            item_loader['市'] = "湖北"
            item_loader['网站名称'] = "湖北省建筑施工企业信用体系建设平台"
            item_loader['url'] = response.urljoin(tr.xpath("./td[2]/a/@href").extract_first())

            yield item_loader


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--93'.split())
