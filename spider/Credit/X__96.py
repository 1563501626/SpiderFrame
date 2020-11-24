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
    name = 'X--96'
    filter_data = True
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': '115.233.209.150:88',
        'Origin': 'http://115.233.209.150:88',
        'Referer': 'http://115.233.209.150:88/index.aspx?tabid=debbe13c-ebc0-4241-90dc-65ffc83233af',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',}
    data = {
       '__EVENTTARGET': '',
       '__EVENTARGUMENT': '',
       '__VIEWSTATE': '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',
       '__VIEWSTATEGENERATOR': '90059987',
       '__EVENTVALIDATION': 'RErwpXTiN96wt2HJE/AK9Ib91xAhDgs4lUH623Ri3Sa6lJ3v7ubMzWN+tY3/RAauQFReWMGnTfJlA6/D2zgK4qUswi6x78qDX7AbL1hlxb6M/xJM2dtBrOBC6DUErLlNSL+SlEVw45WrPKrIJQWmpW5Zbotexy5lPm5FFQO7G5rAmCIr1DV4zwL2pN+Ykzk4JeoBEQ==',
       '_ctl9:txtEnterTitle': '',
       '_ctl9:txtEnterName': '',
       '_ctl9:dateBegin:foo': datetime.datetime.now().strftime('%F'),
       '_ctl9:dateBegin:txtstype': '',
       '_ctl9:dateEnd:foo': datetime.datetime.now().strftime('%F'),
       '_ctl9:dateEnd:txtstype': '',
       '_ctl9:btnEnterprise': '',
       '_ctl9:txtGotoPage': '',
    }
    start_urls = ['http://115.233.209.150:88/index.aspx?tabid=debbe13c-ebc0-4241-90dc-65ffc83233af']
    url = 'http://115.233.209.150:88/index.aspx?tabid=debbe13c-ebc0-4241-90dc-65ffc83233af'
    download_delay = float(gConfig.sleep_time)

    def parse(self, response):
        self.data['__VIEWSTATE'] = response.xpath("//input[@name='__VIEWSTATE']/@value").extract_first("")
        self.data['__EVENTVALIDATION'] = response.xpath("//input[@name='__EVENTVALIDATION']/@value").extract_first("")
        yield scrapy.FormRequest(
            url=self.url,
            method='post',
            formdata=self.data,
            callback=self.deal_parse,
            dont_filter=True,
            headers=self.headers
        )

    def deal_parse(self, response):
        trs = response.xpath("//table[@class='Winstar-table']/tr[position()>1]")
        for tr in trs:
            meta = {}
            meta['标题'] = tr.xpath("./td[1]/a/text()").extract_first("").strip()
            meta['企业名称'] = tr.xpath("./td[2]/text()").extract_first("").strip()
            meta['企业类型'] = tr.xpath("./td[3]/text()").extract_first("").strip()
            meta['分值'] = tr.xpath("./td[4]/text()").extract_first("").strip()
            meta['发文时间'] = tr.xpath("./td[5]/text()").extract_first("").strip()
            url = response.urljoin(tr.xpath("./td[1]/a/@href").extract_first())
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                dont_filter=True,
                callback=self.parse_detail,
                meta=meta
            )

    def parse_detail(self, response):
        meta = response.meta
        item_loader = AutoItem()
        item_loader['标题'] = meta['标题']
        item_loader['企业名称'] = meta['企业名称']
        item_loader['企业类型'] = meta['企业类型']
        item_loader['分值'] = meta['分值']
        item_loader['发文时间'] = meta['发文时间']
        item_loader['项目名称'] = response.xpath("//span[@id='lblName']/text()").extract_first("").strip()
        item_loader['颁奖单位'] = response.xpath("//td[@class='rightd'][contains(string(), '颁奖单位')]/following-sibling::td[1]/span[@id='lblPunishDept']/text()").extract_first("").strip()
        item_loader['处罚部门'] = response.xpath("//td[@class='rightd'][contains(string(), '处罚部门')]/following-sibling::td[1]/span[@id='lblPunishDept']/text()").extract_first("").strip()
        item_loader['省'] = '浙江'
        item_loader['市'] = '杭州'
        item_loader['网站名称'] = '杭州建设信用监管平台'
        item_loader['评价机构'] = '杭州建设信用监管平台'
        item_loader['url'] = response.url
        trs = response.xpath("//table[@id='TallyList']/tr[position()>1]")
        for tr in trs:
            item_loader['序号'] = tr.xpath("./td[1]/text()").extract_first("").strip()
            item_loader['行为'] = tr.xpath("./td[2]/text()").extract_first("").strip()
            item_loader['类别'] = tr.xpath("./td[3]/text()").extract_first("").strip()
            item_loader['md5'] = ezfuc.md5(item_loader['标题'], item_loader['企业名称'], item_loader['企业类型'],item_loader['分值'],
                                           item_loader['发文时间'], item_loader['项目名称'], item_loader['颁奖单位'], item_loader['处罚部门'],
                                           item_loader['序号'], item_loader['行为'], item_loader['类别'])
            yield item_loader


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--96', 'auto', 1])
