# -*- coding: utf-8 -*-
import scrapy
from spider_code.confs.getConfig import conn
from spider_code.items import AutoItem

import manager


class Spider(manager.Spider):
    name = 'X--25'
    allowed_domains = ['http://115.238.132.42:8000']
    start_urls = ['http://http://115.238.132.42:8000/']
    headers = {
        # 'Host': '115.238.132.42:8000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Content-Length': '105',
        # 'Origin': 'http://115.238.132.42:8000',
        # 'Connection': 'keep-alive',
        'Referer': 'http://115.238.132.42:8000/Public/EnterpriseSearch',
    }
    db = conn("company")

    def start_requests(self):
        sql = "select company_name from x__25_company where company_registered_address='浙江省'"
        items = self.db.query(sql)
        for company_name in items:
            data = {
                "EnterpriseName": company_name['company_name'].strip()
            }
            yield scrapy.FormRequest(
                url="http://115.238.132.42:8000/Public/EnterpriseSearch",
                formdata=data,
                headers=self.headers,
                dont_filter=True
            )

    def parse(self, response):
        items = response.xpath('//table[@class="table-data"]/tbody/tr')
        for it in items:
            企业名称 = it.xpath('td[1]/text()').extract_first('')
            if "无查询结果" != 企业名称:
                评价机构 = "宁波市建筑市场信用系统"
                行业 = ""
                专业 = it.xpath('td[2]/text()').extract_first('')
                信用得分 = it.xpath('td[6]/text()').extract_first('')
                信用等级 = it.xpath('td[7]/text()').extract_first('')
                排名 = ''
                今日得分 = ''
                今日排名 = ''
                六十得分 = ''
                六十日排名 = ''
                评价年度 = ''
                网站维护代码 = 'X--25'
                发布日期 = ''
                有效期 = ""
                省 = "浙江"
                市 = "宁波"
                网站名称 = "宁波市建筑市场信用信息网"
                Url = f'http://115.238.132.42:8000/Public/EnterpriseSearch?EnterpriseName={企业名称}'
                item = AutoItem()
                item['企业名称'] = 企业名称
                item['评价机构'] = 评价机构
                item['行业'] = 行业
                item['专业'] = 专业
                item['信用得分'] = 信用得分
                item['信用等级'] = 信用等级
                item['排名'] = 排名
                item['今日得分'] = 今日得分
                item['今日排名'] = 今日排名
                item['六十日得分'] = 六十得分
                item['六十日排名'] = 六十日排名
                item['评价年度'] = 评价年度
                item['网站维护代码'] = 网站维护代码
                item['发布日期'] = 发布日期
                item['有效期'] = 有效期
                item['省'] = 省
                item['市'] = 市
                item['网站名称'] = 网站名称
                item['url'] = Url
                yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--25', 'auto', 1])
