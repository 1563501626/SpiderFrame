# -*- coding: utf-8 -*-
import scrapy
import random, re
from spider_code.items import CreditItem
import time


import manager
class Spider(manager.Spider):
    name = 'chengdugcztb'
    allowed_domains = ['http://cbs.xmchengdu.gov.cn']
    start_urls = ['http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2']
    custom_settings = {
        "ITEM_PIPELINES": {
            # "XinYongpj_Spider.pipelines.TuniuPipeline":300,
            "XinYongpj_Spider.pipelines.ServerPipeline": 301
        },
        "DOWNLOADER_MIDDLEWARES": {
            "XinYongpj_Spider.middlewares.ProcessAllExceptionMiddleware": 543
        }
    }
    post_data_one = {
        "ScriptManager1": "UpdatePanel2|AspNetPager_XWList",
        "txt_lb": "",
        "txt_key": "",
        "AspNetPager_XWList_input": "1",
        "AspNetPager_XWList2_input": "1",
        "AspNetPager_XWList3_input": "1",
        "AspNetPager_XWList4_input": "1",
        # "__VIEWSTATE":"",
        "__EVENTTARGET": "AspNetPager_XWList",
        "__EVENTARGUMENT": "1",
        # "__EVENTVALIDATION":"",
        "__ASYNCPOST": "true",
        "btnLook":""
    }
    post_data = {
        "ScriptManager1": "UpdatePanel4|AspNetPager_XWList2",
        "txt_lb": "",
        "txt_key": "",
        "AspNetPager_XWList_input": "1",
        "AspNetPager_XWList2_input": "1",
        "AspNetPager_XWList3_input": "1",
        "AspNetPager_XWList4_input": "1",
        # "__VIEWSTATE":"",
        "__EVENTTARGET": "AspNetPager_XWList",
        "__EVENTARGUMENT": "1",
        # "__EVENTVALIDATION":"",
        "__ASYNCPOST": "true",
    }
    post_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "cbs.chengdu.com.cn",
        "Referer": "http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    def parse(self, response):
        # print(response.text)
        self.post_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
        self.post_data['__EVENTARGUMENT'] = "1"
        self.post_data['__VIEWSTATE'] = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first('')
        self.post_data['__EVENTVALIDATION'] = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first('')


        # dict_ = {
        #     "sg_sz":"X--11",
        #     "sg_fj": "X--12",
        # }
        # for k, v in dict_.items():
        #     self.post_data['txt_lb'] = k
        #     self.post_data['__EVENTTARGET'] = "AspNetPager_XWList2"
        #     self.post_data['ScriptManager1'] = "UpdatePanel4|AspNetPager_XWList2"
        #     yield scrapy.FormRequest(
        #         url=response.url,
        #         headers=self.post_headers,
        #         meta={
        #             "EVENTARGUMENT": 1,
        #             "txt_lb": k,
        #             "网站维护代码": v
        #         },
        #         formdata=self.post_data,
        #         dont_filter=True,
        #         callback=self.get_sg_sz
        #
        #     )
        #
        #
        # # 13
        # self.post_data['txt_lb'] = "1"
        # self.post_data['__EVENTTARGET'] = "AspNetPager_XWList4"
        # self.post_data['ScriptManager1'] = "UpdatePanel8|AspNetPager_XWList4"
        # yield scrapy.FormRequest(
        #     url=response.url,
        #     headers=self.post_headers,
        #     meta={
        #         "EVENTARGUMENT": 1,
        #     },
        #     formdata=self.post_data,
        #     dont_filter=True,
        #     callback=self.get_fj_szl
        #
        # )
        #
        #
        # dict_ = {
        #     "2":"X--14",
        #     "3":"X--15",
        #     "5":"X--16",
        #     "6":"X--17",
        #     "7":"X--18"
        # }
        # for k, v in dict_.items():
        #     self.post_data['txt_lb'] = k
        #     self.post_data['__EVENTTARGET'] = "AspNetPager_XWList3"
        #     self.post_data['ScriptManager1'] = "UpdatePanel6|AspNetPager_XWList3"
        #     self.post_data['AspNetPager_XWList4_input'] = "1"
        #     yield scrapy.FormRequest(
        #         url=response.url,
        #         headers=self.post_headers,
        #         meta={
        #             "EVENTARGUMENT": 1,
        #             "网站维护代码": v,
        #             "AspNetPager_XWList4_input": "1",
        #             "txt_lb": k,
        #             "ScriptManager1": "UpdatePanel6|AspNetPager_XWList3",
        #             "__EVENTTARGET": "AspNetPager_XWList3"
        #         },
        #         formdata=self.post_data,
        #         dont_filter=True,
        #         callback=self.get_shuili
        #
        #     )

        # X--10
        self.post_data['txt_lb'] = "0"
        self.post_data['__EVENTTARGET'] = ""
        self.post_data['ScriptManager1'] = "ScriptManager1|btnLook"
        # self.post_data['btnLook'] = ""
        self.post_data['__EVENTARGUMENT'] = ""
        yield scrapy.FormRequest(
            url=response.url,
            headers=self.post_headers,
            meta={
                "EVENTARGUMENT": 1
            },
            formdata=self.post_data,
            dont_filter=True,
            callback=self.get_sy
        )


    def get_shuili(self, response):
        # print(response.text)
        li_list = response.xpath('//li[position()>15]')
        for li in li_list:
            企业名称 = li.xpath('div[1]/a/@title').extract_first('')
            评价机构 = "成都市工程建设招标投标从业单位信用信息平台"
            行业 = ''
            专业 = li.xpath('string(div[2])').extract_first('').strip()
            信用得分 = li.xpath('string(div[3])').extract_first('').strip()
            信用等级 = li.xpath('string(div[4])').extract_first('').strip()
            排名 = ''
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = ""
            网站维护代码 = response.meta['网站维护代码']
            发布日期 = ''
            有效期 = ""
            省 = "成都"
            市 = "成都"
            网站名称 = "成都市工程建设招标投标从业单位信用信息平台"
            url = response.url
            encode_md5 = mao_demo_tools.Md5(网站名称 + 企业名称 + 信用等级 + 行业 + url)
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
        pageallcount = re.findall("AspNetPager_XWList3.*?下一页.*?AspNetPager_XWList3','(.+?)'\).*?尾页",response.text, re.S)
        pageCount = response.meta['EVENTARGUMENT']
        print(">>>>>>pageall",pageallcount)
        if pageallcount:
        # # if pageCount < int(3):
            self.post_data['__EVENTTARGET'] = response.meta['__EVENTTARGET']
            self.post_data['AspNetPager_XWList_input'] = str(pageCount)
            pageCount += 1
            self.post_data['__EVENTARGUMENT'] = str(pageCount)
            re_set = re.findall("__VIEWSTATE\|(.+?)\|.*?__EVENTVALIDATION\|(.+?)\|", response.text, re.S)[0]
            self.post_data['__VIEWSTATE'] = re_set[0]
            self.post_data['__EVENTVALIDATION'] = re_set[1]
            self.post_data['ScriptManager1'] = response.meta['ScriptManager1']
            self.post_data['txt_lb'] = response.meta['txt_lb']
            self.post_data['AspNetPager_XWList4_input'] = response.meta['AspNetPager_XWList4_input']
            yield scrapy.FormRequest(
                url=response.url,
                headers=self.post_headers,
                meta={
                    "EVENTARGUMENT": pageCount,
                    "网站维护代码": response.meta['网站维护代码'],
                    "AspNetPager_XWList4_input": response.meta['AspNetPager_XWList4_input'],
                    "txt_lb": response.meta['txt_lb'],
                    "ScriptManager1": response.meta['ScriptManager1'],
                    "__EVENTTARGET": response.meta['__EVENTTARGET']
                },
                formdata=self.post_data,
                dont_filter=True,
                callback=self.get_shuili
            )

    def get_fj_szl(self, response):
        li_list = response.xpath('//li[position()>15]')
        for li in li_list:
            企业名称 = li.xpath('div[2]/a/@title').extract_first('')
            评价机构 = "成都市工程建设招标投标从业单位信用信息平台"
            行业 = ''
            专业 = li.xpath('string(div[3])').extract_first('').strip()
            信用得分 = ''
            信用等级 = ''
            排名 = li.xpath('string(div[4])').extract_first('').strip()
            今日得分 = li.xpath('string(div[5])').extract_first('').strip()
            今日排名 = ''
            六十得分 = li.xpath('string(div[6])').extract_first('').strip()
            六十日排名 = ''
            评价年度 = ""
            网站维护代码 = "X--13"
            发布日期 = ''
            有效期 = ""
            省 = "成都"
            市 = "成都"
            网站名称 = "成都市工程建设招标投标从业单位信用信息平台"
            url = response.url
            encode_md5 = mao_demo_tools.Md5(网站名称 + 企业名称 + 信用等级 + 行业 + url)
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
        pageCount = response.meta['EVENTARGUMENT']
        pageAllCount = re.findall('下一页.*?AspNetPager_XWList4\',\'(\d+)\'', response.text, re.S)
        print(">>>>>>pageall", pageAllCount)
        if len(pageAllCount)==2:
        # if pageCount < 3:
            self.post_data['AspNetPager_XWList4_input'] = "1"
            self.post_data['__EVENTTARGET'] = "AspNetPager_XWList4"
            self.post_data['AspNetPager_XWList_input'] = str(pageCount)
            pageCount += 1
            self.post_data['__EVENTARGUMENT'] = str(pageCount)
            re_set = re.findall("__VIEWSTATE\|(.+?)\|.*?__EVENTVALIDATION\|(.+?)\|", response.text, re.S)[0]
            self.post_data['__VIEWSTATE'] = re_set[0]
            self.post_data['__EVENTVALIDATION'] = re_set[1]
            self.post_data['ScriptManager1'] = "UpdatePanel8|AspNetPager_XWList4"
            self.post_data['txt_lb'] = "1"
            yield scrapy.FormRequest(
                url=response.url,
                headers=self.post_headers,
                meta={
                    "EVENTARGUMENT": pageCount
                },
                formdata=self.post_data,
                dont_filter=True,
                callback=self.get_fj_szl
            )

    def get_sg_sz(self, response):
        li_list = response.xpath('//li[position()>15]')
        for li in li_list:
            企业名称 = li.xpath('div[2]/a/@title').extract_first('')
            评价机构 = "成都市工程建设招标投标从业单位信用信息平台"
            行业 = ''
            专业 = ''
            信用得分 = ''
            信用等级 = ''
            排名 = li.xpath('string(div[4])').extract_first('').strip()
            今日得分 = li.xpath('string(div[5])').extract_first('').strip()
            今日排名 = ''
            六十得分 = li.xpath('string(div[6])').extract_first('').strip()
            六十日排名 = ''
            评价年度 = ""
            网站维护代码 = response.meta['网站维护代码']
            发布日期 = ''
            有效期 = ""
            省 = "成都"
            市 = "成都"
            网站名称 = "成都市工程建设招标投标从业单位信用信息平台"
            url = response.url
            encode_md5 = mao_demo_tools.Md5(网站名称 + 企业名称 + 信用等级 + 行业 + url)
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
        pageCount = response.meta['EVENTARGUMENT']
        pageAllCount = re.findall('下一页.*?AspNetPager_XWList2\',\'(\d+)\'', response.text, re.S)
        print(">>>>>>pageall", pageAllCount)
        if len(pageAllCount)==2:
            self.post_data['AspNetPager_XWList4_input'] = "1"
            self.post_data['AspNetPager_XWList_input'] = str(pageCount)
            pageCount += 1
            self.post_data['__EVENTARGUMENT'] = str(pageCount)
            re_set = re.findall("__VIEWSTATE\|(.+?)\|.*?__EVENTVALIDATION\|(.+?)\|", response.text, re.S)[0]
            self.post_data['__VIEWSTATE'] = re_set[0]
            self.post_data['__EVENTVALIDATION'] = re_set[1]
            self.post_data['ScriptManager1'] = "UpdatePanel4|AspNetPager_XWList2"
            self.post_data['__EVENTTARGET'] = "AspNetPager_XWList2"
            self.post_data['txt_lb'] = response.meta['txt_lb']
            yield scrapy.FormRequest(
                url=response.url,
                headers=self.post_headers,
                meta={
                    "EVENTARGUMENT": pageCount,
                    "txt_lb": response.meta['txt_lb'],
                    "网站维护代码": response.meta['网站维护代码']
                },
                formdata=self.post_data,
                dont_filter=True,
                callback=self.get_sg_sz
            )

    def get_sy(self, response):
        li_list = response.xpath('//li')
        for i in li_list:
            企业名称 = i.xpath('div[1]/a/@title').extract_first('')
            评价机构 = "成都市工程建设招标投标从业单位信用信息平台"
            行业 = i.xpath('string(div[2])').extract_first('').strip()
            专业 = i.xpath('string(div[3])').extract_first('').strip()
            信用得分 = i.xpath('string(div[4])').extract_first('').strip()
            信用等级 = i.xpath('string(div[5])').extract_first('').strip()
            排名 = ""
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = ""
            网站维护代码 = "X--10"
            发布日期 = ''
            有效期 = ""
            省 = "成都"
            市 = "成都"
            网站名称 = "成都市工程建设招标投标从业单位信用信息平台"
            url = response.url
            encode_md5 = mao_demo_tools.Md5(网站名称 + 企业名称 + 信用等级 + 行业 + url)
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
        pageCount = response.meta['EVENTARGUMENT']
        pageAllCount = re.findall('下一页.*?AspNetPager_XWList\',\'(\d+)\'', response.text, re.S)
        # print(">>>>>>pageall", pageAllCount)
        if pageAllCount:
        # if pageCount < 3:
            self.post_data['AspNetPager_XWList4_input'] = "1"
            self.post_data['__EVENTTARGET'] = "AspNetPager_XWList"
            self.post_data['AspNetPager_XWList_input'] = str(pageCount)
            pageCount += 1
            self.post_data['__EVENTARGUMENT'] = str(pageCount)
            re_set = re.findall("__VIEWSTATE\|(.+?)\|.*?__EVENTVALIDATION\|(.+?)\|", response.text, re.S)
            if re_set:
                __VIEWSTATE = re_set[0][0]
                __EVENTVALIDATION = re_set[0][1]
            else:
                __EVENTVALIDATION = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first('')
                __VIEWSTATE = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first('')
            self.post_data['__VIEWSTATE'] = __VIEWSTATE
            self.post_data['__EVENTVALIDATION'] = __EVENTVALIDATION
            self.post_data['ScriptManager1'] = "UpdatePanel2|AspNetPager_XWList"
            self.post_data['txt_lb'] = ""
            yield scrapy.FormRequest(
                url=response.url,
                headers=self.post_headers,
                meta={
                    "EVENTARGUMENT": pageCount
                },
                formdata=self.post_data,
                dont_filter=True,
                callback=self.get_sy
            )

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute(["scrapy", 'crawl', 'chengdugcztb'])