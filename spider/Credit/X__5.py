# -*- coding: utf-8 -*-
import scrapy
import re
from spider_code.items import AutoItem


import manager
class Spider(manager.Spider):
    name = 'x--5'
    allowed_domains = ['http://jtt.sc.gov.cn:81']
    start_urls = [
        'http://182.150.21.186:8080/jsscplatemore-good-1',  # 良好
        'http://182.150.21.186:8080/jsscplatemore-bad-1'  # 较差
    ]
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         # "XinYongpj_Spider.pipelines.TuniuPipeline": 300,
    #         "XinYongpj_Spider.pipelines.ServerPipeline": 301
    #     }
    # }
    get_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Host": "182.150.21.186:8080",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    def start_requests(self):
        _dict = {
            # "http://182.150.21.186:8080/syjsscplatemore-mid-": "X--21",
            "http://182.150.21.186:8080/jsscplatemore-mid-": "X--5"
        }
        for k, v in _dict.items():
            url = k + "1"
            yield scrapy.Request(
                url=url,
                headers=self.get_headers,
                meta={"web_code": v},
                dont_filter=True
            )

    def parse(self, response):
        a_list = response.xpath('//div[@class="newAll_box"]/a')
        for a in a_list:
            url = response.urljoin(a.xpath('@href').extract_first(''))
            企业名称 = a.xpath('ol/li[2]/text()').extract_first('')
            信用等级 = a.xpath('ol/li[3]/text()').extract_first('')
            yield scrapy.Request(
                url=url,
                headers=self.get_headers,
                meta={
                    "企业名称": 企业名称,
                    "信用等级": 信用等级,
                    "web_code": response.meta['web_code']
                },
                dont_filter=True,
                callback=self.get_data
            )
        page = response.xpath('//ol[@class="list_page"]/li[last()]/a/@href').extract_first('')
        if "java" not in page:
            url = response.urljoin(page)
            print(url)
            yield scrapy.Request(
                url=url,
                headers=self.get_headers,
                meta={"web_code": response.meta['web_code']},
                dont_filter=True
            )

    def get_data(self, response):
        # print(response.text)
        企业名称 = response.meta['企业名称']
        评价机构 = "四川省交通厅企业信用评价"
        行业 = ""
        专业 = re.findall("企业类型</td>.*?<td>(.+?)</td>", response.text, re.S)[0]
        信用得分 = ""
        信用等级 = response.meta['信用等级']
        排名 = ""
        今日得分 = ""
        今日排名 = ""
        六十日得分 = ""
        六十日排名 = ""
        评价年度 = ''
        网站维护代码 = response.meta['web_code']
        发布日期 = ''
        有效期 = ''
        省 = "四川"
        市 = "四川"
        网站名称 = "信用交通·四川"
        url = response.url
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
        item['六十日得分'] = 六十日得分
        item['六十日排名'] = 六十日排名
        item['评价年度'] = 评价年度
        item['网站维护代码'] = 网站维护代码
        item['发布日期'] = 发布日期
        item['有效期'] = 有效期
        item['省'] = 省
        item['市'] = 市
        item['网站名称'] = 网站名称
        item['url'] = url
        # item['update_code'] = "0"
        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl x--5'.split())
