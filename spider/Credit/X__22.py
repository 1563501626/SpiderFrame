# -*- coding: utf-8 -*-
import scrapy
import re
import time

from fuclib import ezfuc

from spider_code.items import AutoItem


import manager
class Spider(manager.Spider):
    name = 'X--22'
    filter_data = True
    allowed_domains = ['http://jssccx.zjt.gov.cn:8532']
    start_urls = ['http://http://jssccx.zjt.gov.cn:8532/']
    post_data = {}

    def start_requests(self):
        items_dict = {
            "X--22":"1",
            # "X--23":"2",
        }
        for website_code,levelType in items_dict.items():
            self.post_data['year'] = "2019"
            self.post_data['levelType'] = levelType
            self.post_data['corpName'] = ""
            print(self.post_data)
            yield scrapy.FormRequest(
                url = "http://jssccx.zjt.gov.cn:8532/index/sg_credit_list.htm",
                meta={"currentPage":1,"levelType":levelType,"website_code":website_code},
                formdata=self.post_data,
                dont_filter=True
            )


    def parse(self, response):
        website_code = response.meta['website_code']
        items = response.xpath('//table[@class="s-table-list"]/tr[position()>1]')
        for it in items:
            企业名称 = it.xpath('td[2]/text()').extract_first('')
            评价机构 = "浙江省交通运输厅"
            行业 = ""
            专业 = ''
            信用得分 = ''
            信用等级 = it.xpath('td[3]/text()').extract_first('')
            排名 = ''
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = it.xpath('td[5]/text()').extract_first('')
            网站维护代码 = website_code
            发布日期 = ''
            有效期 = ""
            省 = "浙江"
            市 = "浙江"
            网站名称 = "浙江省交通厅"
            id_  = re.findall("(\d+)", "openDetailWin('公路工程','59','2015','1')")
            Url = f"http://jssccx.zjt.gov.cn:8532/index/sg_credit_detail.htm?sgUserid={id_[0]}&year={id_[1]}&projectType={id_[2]}"
            encode_md5 = ezfuc.md5(网站名称, 企业名称, 信用等级, 发布日期, Url)
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
            # item['data_time'] = time.strftime("%F")
            item['md5'] = encode_md5
            # item['update_code'] = "0"
            yield item
        page_num = re.findall("页数: \[.*?/(.+?)\] 共.*?条",response.text,re.S)[0]
        levelType = response.meta['levelType']
        currentPage = response.meta['currentPage']
        if currentPage < int(page_num.strip()):
            currentPage +=1
            self.post_data['levelType'] = levelType
            self.post_data['currentPage'] = str(currentPage)
            yield scrapy.FormRequest(
                url=response.url,
                formdata=self.post_data,
                meta={"levelType":levelType,"currentPage":currentPage,"website_code":website_code},
                dont_filter=True
            )


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl X--22'.split())