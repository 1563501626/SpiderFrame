# -*- coding: utf-8 -*-
import random

import scrapy
from confs import getConfig
from items import BeianItem

# configuration item
from manager.engine import Engine

gConfig = getConfig.get_config()
"""
建筑业、工程勘察、工程设计、设计施工一体化
"""


class Spider(Engine):
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.name = 'B--3'
        self.start_urls = ["http://202.61.88.188/xxgx/Enterprise/eList.aspx"]
        self.data = {'__VIEWSTATE': '/wEPDwUHOTE0NTIwM2RkjGC6Nvr4LEQhDdxRAPtAjKyhm+f5gVfuI8f1QwTapmk=',
                '__VIEWSTATEGENERATOR': '329B2EFC',
                '__EVENTVALIDATION': '/wEdAAKMcign9KBLHMxtX3C8ZyaE+d3fBy3LDDz0lsNt4u+CuCy5ooogZX46IdczaboOyeWFpDacyfPYqx9jh8bmcega',
                'qylx': '101', 'mc': '司', 'xydm': '', 'fr': '', 'zsbh': '', 'ctl00$MainContent$Button1': '搜索'}
        # filter_data = True  # 去重
        self.filter_db = "duplicate_key"  # md5存储库
        self.filter_table = "beian_b__3"  # md5存储表
        self.db = getConfig.company_name_db()
        self.url = "http://202.61.88.188/xxgx/Enterprise/eList.aspx"
        self.key_map = {
            "101": "建筑业",
            "102": "工程勘察",
            "103": "工程设计",
            "108": "设计施工一体化"
        }
        self.base = "http://202.61.88.188/xxgx/Enterprise/"
        self.custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'spider_code.middlewares.ProxyMiddleware': 543,
                # 'spider_code.middlewares.SpiderCodeDownloaderMiddleware': 542,
            },
            'DOWNLOAD_TIMEOUT': 60
        }
        self.timeout = 10
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '402',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': '202.61.88.188',
            'Origin': 'http://202.61.88.188',
            'Referer': 'http://202.61.88.188/xxgx/Enterprise/eList.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.116Safari/537.36',
        }

    def parse(self, response):
        start = 0
        step = 10000
        count = self.db.query("select count(*) c from company_name_copy where IsLock_Beian=1")[0]['c']
        count = self.db.query("select count(*) c from company_name")[0]['c']
        print(count)
        if start < count:
            # companies = self.db.query("select company_name from company_name_copy where IsLock_Beian=1")
            companies = self.db.query("select 企业名称, id from company_name")
            for company in companies:
                for key in self.key_map.keys():
                    self.headers['X-Real-IP'] = f"{random.randint(1, 200)}.{random.randint(1, 200)}.{random.randint(1, 200)}.{random.randint(1, 200)}"
                    self.data["mc"] = company['企业名称'].strip()
                    self.data['qylx'] = key
                    yield scrapy.FormRequest(
                        url=self.url,
                        formdata=self.data,
                        dont_filter=True,
                        callback=self.parse_detail,
                        meta={'key': key, 'cnid': company['id'], 'name': company}
                    )
                    break
                break
            start += step

    def parse_detail(self, response):
        urls = response.xpath("//div[@class='search-result']/table/tbody/tr")[:-1]
        print(response.meta['name'])
        for url in urls:
            href = self.base + url.xpath("./td[1]/a/@href").extract_first()
            company_name = url.xpath(".//a/text()").extract_first()
            area = url.xpath("./td[3]/text()").extract_first()
            response.meta['company_name'] = company_name
            response.meta['area'] = area
            yield scrapy.Request(
                url=href,
                dont_filter=True,
                callback=self.gen_items,
                meta=response.meta
            )
            break

    def gen_items(self, response):
        item_loader = BeianItem()
        item_loader["企业名称"] = response.meta["company_name"]
        # item_loader["统一社会信用代码"] = response.xpath("//th[text()='统一社会信用代码']/following::td[1]/text()").extract_first()
        item_loader["企业链接地址"] = response.url
        item_loader["所属地区"] = response.meta['area']
        # item_loader["企业法定代表人"] = response.xpath("//th[text()='法定代表人']/following::td[1]/text()").extract_first()
        item_loader["企业类型"] = self.key_map[response.meta['key']]
        item_loader["注册地址"] = response.xpath("//th[text()='注册地址']/following::td[1]/text()").extract_first()
        item_loader["采集来源省"] = "四川"
        item_loader["省内或省外"] = "省内+省外"
        item_loader["来源网站"] = "四川省住房和城乡建设厅网工程建设领域项目信息和信用信息公开共享专栏"
        item_loader["网站代码"] = "B--3"

        # item_loader['md5'] = ezfuc.md5(item_loader["企业名称"], item_loader["所属地区"], item_loader["企业类型"], item_loader["注册地址"])
        yield item_loader
        # self.db.query("update company_name_copy set IsLock_Beian=1 where company_name='%s'" % item_loader["企业名称"])
        self.db.insert("beian_company", {"name": 'B--3', 'cnid': response.meta['cnid']})


if __name__ == '__main__':
    from manager.run import run

    run(["spider/BeiAn/B__3.py", "w", 1])
