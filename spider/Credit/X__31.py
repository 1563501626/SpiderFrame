# -*- coding: utf-8 -*-
import scrapy
from spider_code.confs import getConfig
from spider_code.items import CreditItem
import re

# configuration item
gConfig = getConfig.get_config()


import manager
class Spider(manager.Spider):
    name = 'X--31'
    start_urls = [
        'http://xyxt.ahtongtu.cn:10005/website/CreditList.aspx?page=1']
    download_delay = 1.0
    page = 1
    total = 0

    def parse(self, response):
        if not self.total:
            self.total = re.search(r"page=(\d+)", response.xpath("//a[text()='尾页']/@href").extract_first()).group(1)
        self.parse_detail(response)
        for i in range(2, int(self.total)):
            url = 'http://xyxt.ahtongtu.cn:10005/website/CreditList.aspx?page=' + str(i)
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                callback=self.parse_detail,
                )

    def parse_detail(self, response):
        lis = response.xpath("//table[@class='tableList']/tr")
        for i in lis:
            item = CreditItem()
            item["企业名称"] = i.xpath("./td[2]/a/text()").extract_first('').strip()
            item["统一社会信用代码"] = i.xpath("./td[3]/a/text()").extract_first('').strip()
            item["年份"] = i.xpath("./td[4]/text()").extract_first('').strip()
            item["履约得分"] = i.xpath("./td[5]/text()").extract_first('').strip()
            item["投标得分"] = i.xpath("./td[6]/text()").extract_first('').strip()
            item["其他扣分"] = i.xpath("./td[7]/text()").extract_first('').strip()
            item["综合得分"] = i.xpath("./td[8]/text()").extract_first('').strip()
            item["信用等级"] = i.xpath("./td[9]/text()").extract_first('').strip()
            item["备注"] = i.xpath("./td[10]/text()").extract_first('').strip()
            item["网站维护代码"] = self.name
            item["省"] = "安徽"
            item["市"] = "安徽"
            item["网站名称"] = "安徽省公路建设市场信用信息管理系统"
            item['url'] = response.url
            yield item
            # print(item)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--31'.split())
