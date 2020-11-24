# -*- coding: utf-8 -*-
import scrapy
import json,time

from fuclib import ezfuc

from spider_code.items import AutoItem


import manager
class Spider(manager.Spider):
    name = 'X--6'
    filter_data = True
    allowed_domains = ['http://202.61.89.33:16003']
    # start_urls = ['http://http://202.61.89.33:16003/']
    post_data = {
        "unitName":"",
        "aodata":'[{"name":"sEcho","value":1},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":20},{"name":"mDataProp_0","value":"rowNum"},{"name":"mDataProp_1","value":"unitName"},{"name":"mDataProp_2","value":"grade"},{"name":"mDataProp_3","value":"score"},{"name":"mDataProp_4","value":"evaOrg"},{"name":"mDataProp_5","value":"evaYear"}]'
    }
    post_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "202.61.89.33:16003",
        "Referer": "http://202.61.89.33:16003/DMGeoZZZXPortal/evaluate.html",
        "Connection": "keep-alive"
    }

    def start_requests(self):
        self.post_data['aodata'] = '[{"name":"sEcho","value":1},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":20},{"name":"mDataProp_0","value":"rowNum"},{"name":"mDataProp_1","value":"unitName"},{"name":"mDataProp_2","value":"grade"},{"name":"mDataProp_3","value":"score"},{"name":"mDataProp_4","value":"evaOrg"},{"name":"mDataProp_5","value":"evaYear"}]'
        self.post_headers['User-Agent'] = ezfuc.random_ua()
        url = "http://202.61.89.33:16003/DMGeoGTBizServer2/public/UnitAction.do?method=queryGradeGrid"
        yield scrapy.FormRequest(
            url=url,
            headers=self.post_headers,
            formdata=self.post_data,
            dont_filter=True
        )

    def parse(self, response):
        totalnum = json.loads(response.text)['iTotalRecords']
        if int(totalnum)%20 == 0:
            pagecount = int(totalnum)//20
        else:
            pagecount = int(totalnum) // 20+1
        for i in range(1,pagecount+1):
            self.post_headers['User-Agent'] = ezfuc.random_ua()
            self.post_data['aodata'] = '[{"name":"sEcho","value":%s},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":%s},{"name":"iDisplayLength","value":20},{"name":"mDataProp_0","value":"rowNum"},{"name":"mDataProp_1","value":"unitName"},{"name":"mDataProp_2","value":"grade"},{"name":"mDataProp_3","value":"score"},{"name":"mDataProp_4","value":"evaOrg"},{"name":"mDataProp_5","value":"evaYear"}]'%(i,(i-1)*20)
            url = "http://202.61.89.33:16003/DMGeoGTBizServer2/public/UnitAction.do?method=queryGradeGrid"
            yield scrapy.FormRequest(
                url=url,
                headers=self.post_headers,
                formdata=self.post_data,
                dont_filter=True,
                callback=self.get_data
            )

    def get_data(self, response):
        content_list = json.loads(response.text)['aaData']
        for item in content_list:
            企业名称 = item['unitName']
            评价机构 = "四川省政府投资地质灾害防治项目建设市场信用平台"
            行业 = ""
            专业 = ""
            信用得分 = item['score']
            信用等级 = item['grade']
            排名 = ""
            今日得分 = ''
            今日排名 = ''
            六十日得分 = ''
            六十日排名 = ''
            评价年度 = item['evaYear']
            网站维护代码 = 'X--6'
            发布日期 = ''
            有效期 = ""
            省 = "四川"
            市 = "四川"
            网站名称 = "四川省政府投资地质灾害防治项目建设市场信用平台"
            url = "http://202.61.89.33:16003/DMGeoZZZXPortal/evaluate.html"
            encode_md5 = ezfuc.md5(网站名称, 企业名称, 信用等级, 评价年度, url)
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
            item['md5'] = encode_md5
            yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(['scrapy', 'crawl', 'X--6'])