# -*- coding: utf-8 -*-
import re

from manager.engine import Engine
import json
from fuclib import ezfuc
from parsel import Selector

from spider_code.confs import getConfig
from spider_code.items import CreditItem

gConfig = getConfig.get_config()


class Spider(Engine):
    name = 'X--81'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://ciac.zjw.sh.gov.cn/SHCreditInfoInterWeb/CreditBookAnounce/GetQyCreditReportAll2020?page=1&qyNam=&qyzjCode=']
        self.url = 'https://ciac.zjw.sh.gov.cn/SHCreditInfoInterWeb/CreditBookAnounce/GetQyCreditReportAll2020?page={page}&qyNam=&qyzjCode='
        self.headers = {'Accept': 'application/json,text/javascript,*/*;q=0.01',
                        'Accept-Encoding': 'gzip,deflate,br',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Connection': 'keep-alive',
                        'Host': 'ciac.zjw.sh.gov.cn',
                        'Referer': 'https://ciac.zjw.sh.gov.cn/SHCreditInfoInterWeb/CreditBookAnounce/QyCreditReportIndex',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/84.0.4147.105Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest6',}
        self.total = 0
        self.total_count = 0
        self.page = 1

    def parse(self, response):
        result = json.loads(response.text)
        html = Selector(result['resultdata'])
        if not self.total:
            self.total = int(html.xpath("//label[@id='zongyeshu']/text()").extract_first('0').strip())
        if not self.total_count:
            self.total_count = re.search(r"总数：(\d+)条", result['resultdata']).group(1)
        content_li = html.xpath("//table[@class='tablelist table-middle']/tbody/tr")
        for i in content_li:
            item = CreditItem()
            item['企业名称'] = i.xpath("./td[2]/text()").extract_first("").strip()
            item['评价机构'] = "上海市在沪建筑业企业信用评价管理平台"
            item['信用得分'] = i.xpath("./td[3]/text()").extract_first("").strip()
            item['网站维护代码'] = "x--81"
            item['发布日期'] = i.xpath("./td[4]/text()").extract_first("").strip()
            item['省'] = "上海"
            item['市'] = "上海"
            item['网站名称'] = "上海市住房和城乡建设管理委员会"
            item['url'] = response.urljoin(i.xpath("./td[3]/a/@href").extract_first("").strip())
            self.pipeline(item)

        while self.page < self.total:
            self.page += 1
            self.produce(
                url=self.url.format(page=self.page),
                headers=self.headers,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        result = json.loads(response.text)
        html = Selector(result['resultdata'])
        content_li = html.xpath("//table[@class='tablelist table-middle']/tbody/tr")
        for i in content_li:
            item = CreditItem()
            item['企业名称'] = i.xpath("./td[2]/text()").extract_first("").strip()
            item['评价机构'] = "上海市在沪建筑业企业信用评价管理平台"
            item['信用得分'] = i.xpath("./td[3]/text()").extract_first("").strip()
            item['网站维护代码'] = "x--81"
            item['发布日期'] = i.xpath("./td[4]/text()").extract_first("").strip()
            item['省'] = "上海"
            item['市'] = "上海"
            item['网站名称'] = "上海市住房和城乡建设管理委员会"
            item['url'] = response.urljoin(i.xpath("./td[3]/a/@href").extract_first("").strip())
            self.pipeline(item)


if __name__ == '__main__':
    from manager.run import run

    run(["Credit", "X--81", "w", 5])
