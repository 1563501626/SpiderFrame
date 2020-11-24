# -*- coding: utf-8 -*-
import scrapy
import re


import re,datetime

import manager
class Spider(manager.Spider):
    name = 'chongq'
    allowed_domains = ['http://203.93.109.52:8088']
    start_urls = ['http://http://203.93.109.52:8088/']

    def start_requests(self):
        yearList = [
            "1992","1994",'1996','1997','1998','2001','2002','2003','2004','2007','2009','2010',
            '20011','2012','2013','2014','2015','2016','2017','2018','2019','2020'
        ]
        gradeList = ["AA","A","B",'C',"D"]
        item_dict = {
            "3":"X--57",#
            "2":"X--58"#
        }
        for corptype,website_code in item_dict.items():
            for year in yearList:
                for grade in gradeList:
                    url = f"http://203.93.109.52:8088/gl/common/gl/evalresult/list?corpname=&period_code={year}&corptype={corptype}&grade={grade}"
                    yield scrapy.Request(
                        url,
                        meta={"website_code":website_code,"pageNo":0,'year':year,"corptype":corptype,"grade":grade},
                        dont_filter=True
                    )

    def parse(self, response):
        website_code = response.meta['website_code']
        items = response.xpath('//table[@id="sample-table-1"]/tbody/tr')
        for it in items:
            企业名称 = it.xpath('td[2]/a/text()').extract_first('')
            评价机构 = "重庆市公路建设市场信用信息管理系统"
            行业 = ''
            专业 = it.xpath('string(td[4])').extract_first('').strip()
            信用得分 = ''
            信用等级 = it.xpath('td[6]/text()').extract_first('').strip()
            排名 = ""
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = it.xpath('td[5]/text()').extract_first('')
            网站维护代码 = website_code
            发布日期 = ''
            有效期 = ""
            省 = "重庆"
            市 = "重庆"
            网站名称 = "重庆市公路建设市场信用信息管理系统"
            url = response.urljoin(it.xpath('td[2]/a/@href').extract_first(''))
            encode_md5 = Md5(网站名称 + 企业名称 + str(信用得分) + 行业 + url)
            item = ProjectItem()
            item['企业名称'] = 企业名称
            item['评价机构'] = 评价机构
            item['行业'] = 行业
            item['专业'] = 专业
            item['信用得分'] = 信用得分
            item['信用等级'] = 信用等级
            item['排名'] = 排名
            item['今日得分'] = 今日得分
            item['今日排名'] = 今日排名
            item['六十得分'] = 六十得分
            item['六十日排名'] = 六十日排名
            item['评价年度'] = 评价年度
            item['网站维护代码'] = 网站维护代码
            item['发布日期'] = 发布日期
            item['有效期'] = 有效期
            item['省'] = 省
            item['市'] = 市
            item['网站名称'] = 网站名称
            item['url'] = url
            item['data_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            item['encode_md5'] = encode_md5
            item['update_code'] = "0"
            yield item
        page_num = re.findall("总共.*?条记录，.*?/(\d+)页",response.text,re.S)[0]
        pageNo = response.meta['pageNo']
        pageNo+=1
        if pageNo<int(page_num):
            grade = response.meta['grade']
            corptype = response.meta['corptype']
            year = response.meta['year']
            url = f"http://203.93.109.52:8088/gl/common/gl/evalresult/list?corpname=&period_code={year}&corptype={corptype}&grade={grade}&page={pageNo}&"
            yield scrapy.Request(
                url,
                meta={"website_code":website_code , "pageNo": pageNo,'year':year,"corptype":corptype,"grade":grade},
                dont_filter=True
            )
