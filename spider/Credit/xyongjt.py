# -*- coding: utf-8 -*-
import scrapy
import json,time

import manager
class Spider(manager.Spider):
    name = 'xyongjt'
    allowed_domains = ['http://218.85.65.4:30050']
    start_urls = ['http://http://218.85.65.4:30050/']
    post_data = {
        "_condition":"[]",
        "_conditionCache":"",
        "_isCount":"true",
        "_metadata":'[{"name":"orgCode"},{"name":"unitName"},{"name":"period"},{"name":"unitLevel"},{"name":"displayEvaluationObjectType"}]',
        "_size":"5",
        "_sort":'{"orgCode":"desc"}',
        "_total":"0",
        "_page":"1"
    }

    def start_requests(self):
        url = "http://218.85.65.4:30050/gzwz/creditInfoQuery/vwConsCreditEvaluation/list.action"
        yield scrapy.FormRequest(
            url=url,
            formdata=self.post_data,
            dont_filter=True
        )

    def parse(self, response):
        items = json.loads(response.text)
        for it in items['result']['content']:
            企业名称 = it['unitName']
            评价机构 = "信用交通—福建"
            行业 = ""
            专业 = it['displayEvaluationObjectType']
            信用得分 = ''
            信用等级 = it['unitLevel']
            排名 = ''
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = it['period']
            网站维护代码 = 'X--43'
            发布日期 = ''
            有效期 = ""
            省 = "福建"
            市 = "福建"
            网站名称 = "信用交通—福建"
            encode_md5 = Md5(网站名称, 企业名称,信用等级,发布日期)
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
            item['url'] = 'http://218.85.65.4:30050/gzwz/#page-3'
            item['data_time'] = time.strftime("%F")
            item['encode_md5'] = encode_md5
            item['update_code'] = "0"
            yield item
        page_num = items['result']['totalPages']
        pageNo = items['result']['number']
        if page_num != pageNo:
            self.post_data['_page'] = str(pageNo+1)
            yield scrapy.FormRequest(
                url=response.url,
                formdata=self.post_data,
                dont_filter=True
            )
