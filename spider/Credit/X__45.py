# -*- coding: utf-8 -*-
import datetime

import scrapy
import json, time, math

from fuclib import ezfuc

from spider_code.items import AutoItem


import manager
class Spider(manager.Spider):
    name = 'X--45'
    filter_data = True
    allowed_domains = ['220.160.52.164:98']
    start_urls = ['http://220.160.52.164:98/']
    post_data_four = {
        "CSEPNAME": "",
        "CITY": "",
        "page": "1",
        "rows": "15"
    }
    SEASON_dict = {}
    month = datetime.datetime.now().month
    if 3 <= month < 6:
        SEASON_dict['1'] = "第一季度"
    elif 6 <= month < 9:
        SEASON_dict['2'] = "第二季度"
    elif 9 <= month < 12:
        SEASON_dict['3'] = "第三季度"
    else:
        SEASON_dict['4'] = "第四季度"

    def start_requests(self):

        items = {
            "X--45": "http://220.160.52.164:98/yllh/PJXX/JdpjTable",
        }
        for website_code, url in items.items():
            # for year in ["2018","2019","2017",'2016','2015','2020']:
            for year in [str(datetime.datetime.now().year)]:
                # for SEASON in ['1','2','3','4']:
                for SEASON in self.SEASON_dict.keys():
                    self.post_data_four['page'] = '1'
                    self.post_data_four['SEASON'] = SEASON
                    self.post_data_four['YEAR'] = year
                    yield scrapy.FormRequest(
                        url=url,
                        formdata=self.post_data_four,
                        meta={"page": 1, "website_code": website_code, "SEASON": SEASON, "year": year},
                        dont_filter=True
                    )

    def parse(self, response):
        website_code = response.meta['website_code']
        SEASON = response.meta['SEASON']
        year = response.meta['year']
        items = json.loads(response.text)
        for it in items['rows']:
            企业名称 = it['CORPNAME']
            评价机构 = "福建省园林绿化施工企业信用评价系统"
            行业 = ""
            专业 = ""
            信用得分 = str(it['SCORE'])
            信用等级 = ''
            排名 = str(it["RANK"])[:-2]
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = year + '，' + self.SEASON_dict[SEASON]
            网站维护代码 = website_code
            发布日期 = ''
            有效期 = ""
            省 = "福建"
            市 = "福建"
            网站名称 = "福建省园林绿化施工企业信用评价系统"
            CORPID = str(it["CORPID"])[:-2]
            SCOREID = str(it["SCOREID"])
            url = f'http://220.160.52.164:98/yllh/PJXX/JdPjmx?ID={SCOREID}&YEAR={str(it["YEAR"])[:-2]}&SEASON={str(it["QUARTER"])[:-2]}&CID={CORPID}'
            encode_md5 = ezfuc.md5(网站名称, 企业名称, 信用得分, response.url, 评价年度)
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
            item['url'] = url
            item['md5'] = encode_md5
            yield item
        pageNo = response.meta['page']
        page_num = math.ceil(int(items['total']) / 15)
        print(">>>>?", pageNo, page_num)
        if pageNo < int(page_num):
            pageNo += 1
            self.post_data_four['page'] = str(pageNo)
            self.post_data_four['SEASON'] = SEASON
            self.post_data_four['YEAR'] = year
            yield scrapy.FormRequest(
                url=response.url,
                formdata=self.post_data_four,
                meta={"page": pageNo, "website_code": website_code, "SEASON": SEASON, "year": year},
                dont_filter=True
            )


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--45', 'auto', 1])
