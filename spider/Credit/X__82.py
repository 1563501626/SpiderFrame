# -*- coding: utf-8 -*-
from manager.engine import Engine
import json
from parsel import Selector

from spider_code.confs import getConfig
from spider_code.items import CreditItem

gConfig = getConfig.get_config()


class Spider(Engine):
    name = 'X--82'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.url = 'http://zzxs.ciac.sh.cn/XSCreditInfoInterWeb/CreditBookAnounce/GetQyCreditReportAll?page=1&qyNam={name}&qyzjCode='
        self.total = 0
        self.total_count = 0
        self.page = 1

    def start_requests(self):
        companies = getConfig.get_company_from_txt("credit_上海企业")
        for company in companies:
            self.produce(
                url=self.url.format(name=company)
            )

    def parse(self, response):
        result = json.loads(response.text)
        html = Selector(result['resultdata'])
        ret = html.xpath("//table/tbody/tr")
        for i in ret:
            item = CreditItem()
            item['企业名称'] = i.xpath("./td[2]/text()").extract_first("").strip()
            item['评价机构'] = "上海市在沪建筑业企业信用评价管理平台"
            item['信用得分'] = i.xpath("./td[3]/text()").extract_first("").strip()
            item['网站维护代码'] = "x--82"
            item['发布日期'] = i.xpath("./td[4]/text()").extract_first("").strip()
            item['省'] = "上海"
            item['市'] = "上海"
            item['网站名称'] = "上海市住房和城乡建设管理委员会"
            item['url'] = "http://zzxs.ciac.sh.cn" + i.xpath("./td[3]/a/@href").extract_first("").strip()
            self.pipeline(item)


if __name__ == '__main__':
    from manager.run import run

    run(['Credit', 'X--82', 'auto', 1])
