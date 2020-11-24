# -*- coding: utf-8 -*-
import scrapy
import time,re,math

import manager
class Spider(manager.Spider):
    name = 'X--47'
    allowed_domains = ['zjcs.yn.gov.cn']
    start_urls = ['https://zjcs.yn.gov.cn/yns/zjfw/agentList?listVo.sortType=haoping']
    post_data = {
        "listVo.sortType":"haoping",
        "listVo.name":"",
        "listVo.organizationType":"",
        "listVo.divisionCode":"",
        "listVo.serviceType":"",
        "listVo.pubServiceLevel":"",
        "listVo.isBadRecord":"",
    }

    def start_requests(self):
        items = {
            "云南企业投资审批中介超市-地质灾害治理工程设计企业":"053",
            "云南企业投资审批中介超市-地质灾害危险性评估企业":"003",
            "云南企业投资审批中介超市-工程设计企业":"007",
            "云南企业投资审批中介超市-文物保护工程勘察设计企业":"007",
        }
        for zy,serviceType in items.items():
            self.post_data['listVo.serviceType'] = serviceType
            url = "https://zjcs.yn.gov.cn/yns/zjfw/agentList"
            yield scrapy.FormRequest(
                url,
                formdata=self.post_data,
                meta={"pageNo":0,"zy":zy},
                dont_filter=True
            )

    def parse(self, response):
        items = response.xpath('//div[@class="pannel noborder"]//tr[position()>1]')
        for item in items:
            企业名称 = item.xpath('td[1]/a/text()').extract_first('')
            评价机构 = "云南企业投资审批中介超市"
            行业 = response.meta['zy']
            专业 = ''
            信用得分 = item.xpath('td[5]/div/span/span[3]/text()').extract_first("").strip().translate(str.maketrans('', '',"（）"))
            信用等级 = ''
            排名 = ""
            今日得分 = ''
            今日排名 = ''
            六十得分 = ''
            六十日排名 = ''
            评价年度 = ""
            网站维护代码 = 'X--47'
            发布日期 = ''
            有效期 = ""
            省 = "云南"
            市 = "云南"
            网站名称 = "云南企业投资审批中介超市"
            url = response.urljoin(item.xpath('td[1]/a/@href').extract_first(''))
            encode_md5 = Md5(网站名称 + 企业名称 + 信用等级 + 发布日期 + url)
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
            item['data_time'] = time.strftime("%F")
            item['encode_md5'] = encode_md5
            item['update_code'] = "0"
            yield item
        page_num = re.findall('(\d+)',response.xpath('//div[@id="totalElementsView"]/text()').extract_first(''))[0]
        page_num = math.ceil(int(page_num)/10)
        pageNo = response.meta['pageNo']
        if pageNo < int(page_num):
            pageNo+=1
            self.post_data['pageNumber'] = str(pageNo)
            self.post_data['sourtType'] = ''
            yield scrapy.FormRequest(
                response.url,
                meta={"pageNo": pageNo,"zy":response.meta['zy']},
                formdata=self.post_data,
                dont_filter=True
            )


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute(["scrapy", 'crawl', 'X--47'])