# -*- coding: utf-8 -*-
import scrapy
import json, time, math

from spider_code.items import AutoItem


import manager
class Spider(manager.Spider):
    name = 'X--44'
    allowed_domains = ['http://220.160.52.164:98']
    start_urls = ['http://220.160.52.164:98/']
    post_data = {
        "rows": "15"
    }

    def start_requests(self):
        items = {
            "X--44": "http://220.160.52.164:98/yllh/PJXX/MrpjTable"
        }
        for website_code, url in items.items():
            self.post_data['page'] = '1'
            yield scrapy.FormRequest(
                url=url,
                formdata=self.post_data,
                meta={"page": 1, "website_code": website_code},
                dont_filter=True
            )

    def parse(self, response):
        website_code = response.meta['website_code']
        items = json.loads(response.text)
        for it in items['rows']:
            企业名称 = it['CORPNAME']
            评价机构 = "福建省园林绿化施工企业信用评价系统"
            行业 = ""
            专业 = ""
            信用得分 = ''
            信用等级 = ''
            排名 = ''
            今日得分 = str(it['SCORE'])
            今日排名 = str(it["RANK"])[:-2]
            六十日得分 = ''
            六十日排名 = ''
            评价年度 = ""
            网站维护代码 = website_code
            发布日期 = ''
            有效期 = ""
            省 = "福建"
            市 = "福建"
            网站名称 = "福建省园林绿化施工企业信用评价系统"
            CORPID = str(it["CORPID"])[:-2]
            SCOREID = str(it["SCOREID"])
            url = f'http://220.160.52.164:98/yllh/PJXX/MrpjMx?ID={SCOREID}&TIME={str(it["SCOREDATE"])[:-2]}&CID={CORPID}'
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
            # item['data_time'] = time.strftime("%F")
            # item['encode_md5'] = encode_md5
            # item['update_code'] = "0"
            yield item
        pageNo = response.meta['page']
        page_num = math.ceil(int(items['total']) / 15)
        print(">>>>?", pageNo, page_num)
        if pageNo < int(page_num):
            pageNo += 1
            self.post_data['page'] = str(pageNo)
            yield scrapy.FormRequest(
                url=response.url,
                formdata=self.post_data,
                meta={"page": pageNo, "website_code": website_code},
                dont_filter=True
            )


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--44', 'auto', 1])
