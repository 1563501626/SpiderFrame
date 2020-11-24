# -*- coding: utf-8 -*-
import scrapy
import json,math
import datetime


import manager
class Spider(manager.Spider):
    name = 'yunnan'
    allowed_domains = ['https://jtcx.ynjtt.com']
    start_urls = ['http://https://jtcx.ynjtt.com/']
    # custom_settings = {
    #     "DOWNLOADER_MIDDLEWARES":{
    #         'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    #         "XinYongpj_Spider.middlewares.ProxyMiddleware":543,
    #         "XinYongpj_Spider.middlewares.TestDownloaderMiddleware":543,
    #     }
    # }
    post_data = {
        "rows":"19",
        "busYear":""
    }
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Content-Type":"application/x-www-form-urlencoded;charset=utf-8"
    }

    def start_requests(self):
        url = "https://jtcx.ynjtt.com/appUiIntegration/sysIndex/loadCreidtMoreInfo"
        item_dict = {
            "X--52":{"urlType":"2","busType":"1303"},
            "X--51":{"urlType":"2","busType":"1300"},
            "X--50":{"urlType":"1","busType":"1303"},
            "X--49":{"urlType":"1","busType":"1300"},

        }
        for website_code,item in item_dict.items():
            self.post_data['urlType'] = item['urlType']
            self.post_data['busType'] = item['busType']
            self.post_data['page'] = '0'
            yield scrapy.FormRequest(
                url,
                formdata=self.post_data,
                meta={"website_code":website_code,'item':item,"pageNo":1},
                dont_filter=True
            )

    def parse(self, response):
        website_code = response.meta['website_code']
        it = response.meta['item']
        items = json.loads(response.text)['data']['rows']
        for item in items:
            OrgName = item['OrgName']
            OrgID = item['OrgID']
            yield scrapy.FormRequest(
                url="https://jtcx.ynjtt.com/appUiIntegration/creditFiles/GetOrgInfo",
                meta={"OrgName": OrgName, "website_code": website_code, "orgId": OrgID, 'busType': it['busType'],"OrgID":OrgID},
                formdata={"orgId": OrgID,'SysID': "1"},
                headers=self.headers,
                dont_filter=True,
                callback=self.baseData
            )

        total = int(json.loads(response.text)['data']['total'])
        page_num = math.ceil(total/19)
        pageNo = response.meta['pageNo']
        if pageNo<page_num:
            pageNo+=1
            self.post_data['urlType'] = it['urlType']
            self.post_data['busType'] = it['busType']
            self.post_data['page'] = str(pageNo)
            yield scrapy.FormRequest(
                response.url,
                formdata=self.post_data,
                meta={"website_code": website_code, 'item': it, "pageNo": pageNo},
                dont_filter=True
            )

    def baseData(self, response):
        OrgName = response.meta['OrgName']
        website_code = response.meta['website_code']
        OrgID = response.meta['OrgID']
        busType = response.meta['busType']
        print(response.text)
        rows = json.loads(response.text)['data']['rows']
        if rows:
            EnterpriseType = rows[0]['EnterpriseType']
        else:
            EnterpriseType = ''
        yield scrapy.FormRequest(
            url='https://jtcx.ynjtt.com/appUiIntegration/creditFiles/GetOrgCreditResult',
            meta={"OrgName": OrgName, "website_code": website_code, "orgId": OrgID, 'busType': busType,'EnterpriseType':EnterpriseType},
            formdata={"orgId": OrgID, 'rows': '3', 'SysID': "1"},
            headers=self.headers,
            dont_filter=True,
            callback=self.detail_page
        )


    def detail_page(self, response):
        item = ProjectItem()
        行业 = ''
        排名 = ""
        今日得分 = ''
        今日排名 = ''
        六十得分 = ''
        六十日排名 = ''
        评价年度 = ""
        有效期 = ""
        专业 =response.meta['EnterpriseType']
        信用得分 = ''
        信用等级 = ''
        发布日期 = ''
        省 = "云南"
        市 = "云南"
        网站名称 = "云南省公路水路建设与运输市场信用管理系统"
        网站维护代码 = response.meta['website_code']
        评价机构 = "云南省公路水路建设与运输市场信用管理系统"
        if 网站维护代码 in ['X--49','X--50']:
            url = f"https://jtcx.ynjtt.com/appUiIntegration/creditFiles/main?EnterpriseType={response.meta['busType']}&orgId={response.meta['orgId']}&SysID=1"
        else:
            url = f"https://jtcx.ynjtt.com/appUiIntegration/creditFiles/main?EnterpriseType={response.meta['busType']}&orgId={response.meta['orgId']}&SysID=2"
        企业名称 = response.meta['OrgName']
        encode_md5 = Md5(网站名称 + 企业名称 + str(信用得分) + 行业 + url)
        items = json.loads(response.text)['data']['years']
        if items and 网站维护代码 in ['X--49','X--50']:
            for it in items:
                评价机构 = "云南省公路水路建设与运输市场信用管理系统"
                专业 = it['result'][0]['EvaluateType']
                信用得分 = it['result'][0]['TotalScore']
                信用等级 = it['result'][0]['CreditRating']
                发布日期 = it['year']
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
        else:
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

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute(["scrapy", 'crawl', 'yunnan'])