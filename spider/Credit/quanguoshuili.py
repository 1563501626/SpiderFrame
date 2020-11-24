# -*- coding: utf-8 -*-
import scrapy
import random,re
import hashlib,time

import manager
class Spider(manager.Spider):
    name = 'quanguoshuili'
    allowed_domains = ['http://rcpu.cweun.org/Index.aspx']
    start_urls = ['http://rcpu.cweun.org/JInfo.aspx']
    custom_settings = {
        "ITEM_PIPELINES": {
            # "XinYongpj_Spider.pipelines.TuniuPipeline": 300,
            "XinYongpj_Spider.pipelines.ServerPipeline": 301
        }
    }
    post_headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type":"application/x-www-form-urlencoded",
        "Host":"rcpu.cweun.org",
        "Referer":"http://rcpu.cweun.org/JInfo.aspx",
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    post_data_one = {
        "__EVENTTARGET":"ctl00$ContentPlaceHolder1$lbtSEARCH",
        "__EVENTARGUMENT":"",
        # "__VIEWSTATE":"",
        # "__EVENTVALIDATION":""
        "ctl00$ContentPlaceHolder1$TextBoxUNIT":"",
        "ctl00$ContentPlaceHolder1$TextBoxTYEAR":"",
        "ctl00$ContentPlaceHolder1$TextBoxRESULT":"",
        "ctl00$ContentPlaceHolder1$AspNetPager1_input":"1",
        "hindex":"2"
    }
    post_data_two = {
        "__EVENTTARGET": "ctl00$ContentPlaceHolder1$AspNetPager1",
        "__EVENTARGUMENT": "2",#翻页
        "__VIEWSTATE":"/wEPDwUKLTczNDg5MjQzNA8WCh4GSklOREVYZR4FVFlFQVJlHgZVTkNITk1lHgZSRVNVTFRlHgZoaW5kZXhlFgJmD2QWAgIDD2QWAgIBD2QWBAIEDxYCHgtfIUl0ZW1Db3VudAIUFioCAQ9kFgJmDxUIATE855SY6IKD55yB5rC05Yip5rC055S15YuY5rWL6K6+6K6h56CU56m26Zmi5pyJ6ZmQ6LSj5Lu75YWs5Y+4BuWLmOWvnwNBQUEJ5rC05Yip6YOoBDIwMTcKMjAxNy0xMi0wNgoyMDIwLTEyLTA1ZAICD2QWAmYPFQgBMjPkuK3lsbHluILmsLTliKnmsLTnlLXli5jmtYvorr7orqHlkqjor6LmnInpmZDlhazlj7gG5YuY5a+fA0FBQQnmsLTliKnpg6gEMjAxNwoyMDE3LTEyLTA2CjIwMjAtMTItMDVkAgMPZBYCZg8VCAEzKui0teW3nuecgeawtOWIqeawtOeUteWLmOa1i+iuvuiuoeeglOeptumZogbli5jlr58DQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCBA9kFgJmDxUIATQk6ZW/5rKZ5biC5rC05Yip5rC055S15YuY5rWL6K6+6K6h6ZmiBuWLmOWvnwNBQUEJ5rC05Yip6YOoBDIwMTcKMjAxNy0xMi0wNgoyMDIwLTEyLTA1ZAIFD2QWAmYPFQgBNSrmsZ/opb/nnIHotaPopb/lnJ/mnKjlt6XnqIvli5jmtYvorr7orqHpmaIG5YuY5a+fA0FBQQnmsLTliKnpg6gEMjAxNwoyMDE3LTEyLTA2CjIwMjAtMTItMDVkAgYPZBYCZg8VCAE2KuWbm+W3neecgeawtOWIqeawtOeUteWLmOa1i+iuvuiuoeeglOeptumZogbli5jlr58DQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCBw9kFgJmDxUIATc25qWa6ZuE5qyj5rqQ5rC05Yip55S15Yqb5YuY5a+f6K6+6K6h5pyJ6ZmQ6LSj5Lu75YWs5Y+4BuWLmOWvnwNBQUEJ5rC05Yip6YOoBDIwMTcKMjAxNy0xMi0wNgoyMDIwLTEyLTA1ZAIID2QWAmYPFQgBOCrmtZnmsZ/nnIHpkrHloZjmsZ/nrqHnkIblsYDli5jmtYvorr7orqHpmaIG5YuY5a+fA0FBQQnmsLTliKnpg6gEMjAxNwoyMDE3LTEyLTA2CjIwMjAtMTItMDVkAgkPZBYCZg8VCAE5POeUmOiCg+ecgeawtOWIqeawtOeUteWLmOa1i+iuvuiuoeeglOeptumZouaciemZkOi0o+S7u+WFrOWPuAborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCCg9kFgJmDxUIAjEwM+S4reWxseW4guawtOWIqeawtOeUteWLmOa1i+iuvuiuoeWSqOivouaciemZkOWFrOWPuAborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCCw9kFgJmDxUIAjExKui0teW3nuecgeawtOWIqeawtOeUteWLmOa1i+iuvuiuoeeglOeptumZogborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCDA9kFgJmDxUIAjEyKua0m+mYs+awtOWIqeWLmOa1i+iuvuiuoeaciemZkOi0o+S7u+WFrOWPuAborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCDQ9kFgJmDxUIAjEzJOW4uOW+t+W4guawtOWIqeawtOeUteWLmOa1i+iuvuiuoemZogborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCDg9kFgJmDxUIAjE0JOmVv+aymeW4guawtOWIqeawtOeUteWLmOa1i+iuvuiuoemZogborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCDw9kFgJmDxUIAjE1Kuaxn+ilv+ecgei1o+ilv+Wcn+acqOW3peeoi+WLmOa1i+iuvuiuoemZogborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCEA9kFgJmDxUIAjE2MOmdkuWym+W4guawtOWIqeWLmOa1i+iuvuiuoeeglOeptumZouaciemZkOWFrOWPuAborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCEQ9kFgJmDxUIAjE3KuWbm+W3neecgeawtOWIqeawtOeUteWLmOa1i+iuvuiuoeeglOeptumZogborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCEg9kFgJmDxUIAjE4Nuilv+iXj+iHquayu+WMuuawtOWIqeeUteWKm+inhOWIkuWLmOa1i+iuvuiuoeeglOeptumZogborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCEw9kFgJmDxUIAjE5NualmumbhOaso+a6kOawtOWIqeeUteWKm+WLmOWvn+iuvuiuoeaciemZkOi0o+S7u+WFrOWPuAborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCFA9kFgJmDxUIAjIwKua1meaxn+S5neW3nuayu+awtOenkeaKgOiCoeS7veaciemZkOWFrOWPuAborr7orqEDQUFBCeawtOWIqemDqAQyMDE3CjIwMTctMTItMDYKMjAyMC0xMi0wNWQCFQ9kFgICAQ8WAh4HVmlzaWJsZWgWAmYPZBYCAgEPDxYCHwZoZGQCBQ8PFgYeCFBhZ2VTaXplAhQeC1JlY29yZGNvdW50AqMoHhBDdXJyZW50UGFnZUluZGV4AgFkZGQ=",
        "__EVENTVALIDATION":"/wEdAAWfxRBJSUcauuYhFOhsxY6cDONNT9q8O74A5nAwn459dTNgz4ljMB+HUM0b1NXb7NuWpQt1MUMbPWDhr/bs7JPQFTP9UoY0vNpFkAEN6GUTDQ==",
        "ctl00$ContentPlaceHolder1$TextBoxUNIT": "",
        "ctl00$ContentPlaceHolder1$TextBoxTYEAR": "",
        "ctl00$ContentPlaceHolder1$TextBoxRESULT": "",
        "ctl00$ContentPlaceHolder1$AspNetPager1_input": "1",
        "hindex": ""
    }

    def parse(self, response):
        type_dict = {
            "":"X--1",
            "1":"X--2",
            "2":"X--3"
        }
        for hindex,web_code in type_dict.items():
            VIEWSTATE = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first('')
            self.post_data_one['__VIEWSTATE'] = VIEWSTATE
            EVENTVALIDATION = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first('')
            self.post_data_one['__EVENTVALIDATION'] = EVENTVALIDATION
            self.post_data_one['hindex'] = hindex
            self.post_headers['User-Agent'] = random.choice(ua_list)
            url = "http://rcpu.cweun.org/JInfo.aspx"
            yield scrapy.FormRequest(
                url,
                headers=self.post_headers,
                formdata=self.post_data_one,
                meta={
                    "pageCount":1,
                    "web_code":web_code,
                    "hindex":hindex
                },
                dont_filter=True,
                callback=self.get_data
            )

    def get_data(self, response):
        # print(response.text)
        tr_list = response.xpath('//tbody/tr')
        for tr in tr_list:
            企业名称 = tr.xpath('string(td[2])').extract_first('')
            评价机构 = "全国水利建设市场信用信息平台"
            行业 = ""
            专业 = tr.xpath('td[3]/text()').extract_first('')
            信用得分 = ""
            信用等级 = tr.xpath('td[4]/text()').extract_first('')
            排名 = ""
            今日得分 = ""
            今日排名 = ""
            六十得分 = ""
            六十日排名 = ""
            评价年度 = tr.xpath('td[6]/text()').extract_first('')
            网站维护代码 = response.meta['web_code']
            发布日期 = tr.xpath('td[7]/text()').extract_first('')
            有效期 = tr.xpath('td[8]/text()').extract_first('')
            省 = "国家"
            市 = "国家"
            网站名称 = "全国水利建筑市场信用信息平台"
            url = response.url
            encode_md5 = self.Md5(网站名称+企业名称+信用等级+发布日期+url)
            item = XingYong()
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
            item['data_time'] = time.strftime("%F")
            item['encode_md5'] = encode_md5
            item['update_code'] = "0"
            yield item
        pageallCount = re.findall('class="paginator".*?总数：.*?总页数(.+?)</div', response.text, re.S)[0].strip()
        pageCount = response.meta['pageCount']
        print("pageallCount", pageallCount,pageCount)
        if pageCount < int(pageallCount):
            pageCount +=1
            self.post_data_two["__VIEWSTATE"] = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first('')
            self.post_data_two["__EVENTVALIDATION"] = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first('')
            self.post_data_two['__EVENTARGUMENT'] = str(pageCount)
            self.post_data_two['hindex'] = response.meta['hindex']
            self.post_data_two['ctl00$ContentPlaceHolder1$AspNetPager1_input'] = str(pageCount-1)
            self.post_headers['User-Agent'] = random.choice(ua_list)
            yield scrapy.FormRequest(
                url=response.url,
                headers=self.post_headers,
                formdata=self.post_data_two,
                meta={
                    "pageCount": pageCount,
                    "web_code": response.meta['web_code'],
                    "hindex":response.meta['hindex']
                },
                dont_filter=True,
                callback=self.get_data
            )

    def Md5(self, response):
        h1 = hashlib.md5()
        h1.update(response.encode('utf-8'))
        return h1.hexdigest()
