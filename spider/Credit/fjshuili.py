# -*- coding: utf-8 -*-
import scrapy
import json,time


import manager
class Spider(manager.Spider):
    name = 'fjshuili'
    allowed_domains = ['http://61.154.12.112:9001']
    start_urls = ['http://http://61.154.12.112:9001/']
    post_data = {
        "type":"3,5",
        "count":"0",
        "name":"",
        "area":""
    }
    key_dict= {
        "设计单位":"X--42",
        "施工单位":"X--41",
    }
    def start_requests(self):
        url = 'http://61.154.12.112:9001/Handler/ActionScoreInfoHandler_Public.ashx?flag=GetTopScoreList'
        yield scrapy.FormRequest(
            url,
            formdata=self.post_data,
            dont_filter=True
        )

    def parse(self, response):
        items = json.loads(response.text)
        for it in items:
            name = it['name']
            for i in it['list']:
                企业名称 = i['C_Name']
                评价机构 = "福建省水利建设市场信用评价平台"
                行业 = ""
                专业 = ""
                信用得分 = i['Score']
                信用等级 = ""
                排名 = ""
                今日得分 = ''
                今日排名 = ''
                六十得分 = ''
                六十日排名 = ''
                评价年度 = ""
                发布日期 = ''
                有效期 = ""
                省 = "福建"
                市 = "福建"
                网站名称 = "福建省水利建设市场信用评价平台"
                url = 'http://61.154.12.112:9001/CreditFB_web/ranking.html'
                encode_md5 = Md5(网站名称,企业名称,信用等级,发布日期,url)
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
                item['网站维护代码'] = self.key_dict[name]
                item['发布日期'] = 发布日期
                item['有效期'] = 有效期
                item['省'] = 省
                item['市'] = 市
                item['网站名称'] = 网站名称
                item['url'] = url
                item['data_time'] = time.strftime("%F")
                item['encode_md5'] = encode_md5
                item['update_code'] = "0"
                yield item

