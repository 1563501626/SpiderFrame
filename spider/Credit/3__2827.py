# -*- coding: utf-8 -*-
import re
import scrapy
from fuclib import ezfuc


from spider_code.confs import getConfig
from spider_code.items import AutoItem

gConfig = getConfig.get_config()

import manager
class Spider(manager.Spider):
    name = '3--2827'
    filter_data = True

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://118.122.250.198:82/SysPerson/pubProjectSys/publicity/webShowXZCFList.aspx']
        self.url = 'http://118.122.250.198:82/SysPerson/pubProjectSys/publicity/webShowXZCFList.aspx'
        self.data = {
            '__EVENTTARGET': 'dpPage$btnSure',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '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',
            '__VIEWSTATEGENERATOR': 'D507089E',
            '__EVENTVALIDATION': '/wEdAAquj3qlacOwoML2taq9TSu/Kx7BDYJW5FyoHhtAPGrHvofMaGnWRSBH35UZh40l6FT2Erl9C75NYvNTCiwl8+hc2caH/f/tkD2bkpuVwW8lb+yHpT1OJgynHxzMt8TQ2pI0jNAzh2Mm1TVcy4qHHNyAhmHxbKDJFJfOjmhbbuOXuk45Vm0z7rG6wwfQr+9yIKVJITY0uVv0JmKmPnsKj4ApmcWIlbICXtsmdtl/1EdevaxSfI54r/fo/QbrLH5O+ks=',
            'dpPage$txtSelectPage': '2',
            'dpPage$hdfMaxPageSize': '20',
            'dpPage$hdfTotalRecord': '75',
            'dpPage$hdfPageCount': '4',
            'dpPage$hdfCurrentPage': '1',
        }
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': '118.122.250.198:82',
            'Origin': 'http://118.122.250.198:82',
            'Referer': 'http://118.122.250.198:82/SysPerson/pubProjectSys/publicity/webShowXZCFList.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        }
        self.total = 0
        self.total_count = 0

    def parse(self, response):
        if 'Cookie' not in self.headers:
            self.headers['Cookie'] = response.headers[b'set-Cookie'].decode()
        base = "http://118.122.250.198:82/SysPerson/pubProjectSys/publicity/WebXZCFPersonDetail.aspx?FID="
        if not self.total:
            self.total = int(response.xpath("//span[@id='dpPage_lblTotalPage']/text()").extract_first("").strip())
        if not self.total_count:
            self.total_count = int(response.xpath("//span[@id='dpPage_lblTotalRecord']/text()").extract_first("").strip())
        content_li = response.xpath("//table[@class='list']/tr[position()>1]")
        for i in content_li:
            tax_num = i.xpath("./td[3]/text()").extract_first("").strip()
            begin_date = i.xpath("./td[4]/text()").extract_first("").strip()
            end_date = i.xpath("./td[5]/text()").extract_first("").strip()
            url = base + re.search(r"\('(.*?)'", i.xpath("./td[6]/a/@onclick").extract_first()).group(1)
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                meta={
                    'tax_num': tax_num,
                    "begin_date": begin_date,
                    "end_date": end_date
                },
                callback=self.parse_detail
            )
        if 'page' in response.meta:
            page = response.meta['page']
        else:
            page = 1
        if page < self.total:
            self.data['__EVENTVALIDATION'] = response.xpath("//input[@name='__EVENTVALIDATION']/@value").extract_first()
            self.data['__VIEWSTATE'] = response.xpath("//input[@name='__VIEWSTATE']/@value").extract_first()
            page += 1
            self.data['dpPage$txtSelectPage'] = str(page)
            self.data['dpPage$hdfPageCount'] = str(self.total)
            self.data['dpPage$hdfTotalRecord'] = str(self.total_count)
            self.data['dpPage$hdfCurrentPage'] = str(page-1)
            yield scrapy.FormRequest(
                url=self.url,
                dont_filter=True,
                formdata=self.data,
                meta={'page': page}
            )

    def parse_detail(self, response):
        item = AutoItem()
        item['行政处罚决定书文号'] = response.meta['tax_num']
        item['处罚事由'] = response.xpath("//span[@id='t_CF_SY']/text()").extract_first("").strip()
        item['处罚依据'] = response.xpath("//span[@id='t_CF_YJ']/text()").extract_first("").strip()
        item['处罚相对人名称'] = response.xpath("//span[@id='t_CF_XDR_MC']/text()").extract_first("").strip()
        item['处罚结果'] = response.xpath("//span[@id='t_CF_JG']/text()").extract_first("").strip()
        item['处罚生效期'] = response.xpath("//span[@id='t_CF_SXQ']/text()").extract_first("").strip()
        item['处罚截止期'] = response.xpath("//span[@id='t_CF_JZQ']/text()").extract_first("").strip()
        item['处罚机关'] = response.xpath("//span[@id='t_CF_XZJG']/text()").extract_first("").strip()
        item['网站名称'] = '四川省住房和城乡建设厅'
        item['url'] = response.url
        item['md5'] = ezfuc.md5(item['行政处罚决定书文号'], item['处罚事由'], item['处罚依据'], item['处罚相对人名称'],
                                item['处罚结果'], item['处罚生效期'], item['处罚截止期'], item['处罚机关'])
        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl 3--2827'.split())
