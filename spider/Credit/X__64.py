# -*- coding: utf-8 -*-
import datetime
import time

import scrapy
from spider_code.confs import getConfig
from spider_code.items import CreditItem
from fuclib import format_time
from fuclib import ezfuc
import json

# configuration item
gConfig = getConfig.get_config()


import manager
class Spider(manager.Spider):
    name = 'X--64'
    get_header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'qycx.gzcc.gov.cn:8080',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
    page_header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Connection': 'keep-alive',
                   'Cookie': '__RequestVerificationToken=z3bY42QDnW81VVuSrMA2LvX1zxQoGgflXnieVvdaNm5og9I84EvLJtQ9ubgPNGIeKhcJZHZOQ8XSiuP-Q9uWWrSu1XU_m9OMgxoBvH-xTV41',
                   'Host': 'qycx.gzcc.gov.cn:8080',
                   'Referer': 'http://qycx.gzcc.gov.cn:8080/estimate/toatal',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest',
                   '__RequestVerificationToken': 'DH3CY4a80anVo81vIuiK-t59_Nj8pIEBOIxB0DIUdyMo0Qcn1RMHB6hwNsAOfIj_bhrgYjw50rdEaeytpA4OK6JHDZCHfqguf3oAyDXOTTI1'}
    download_delay = float(gConfig.sleep_time)

    def start_requests(self):
        url = f"http://qycx.gzcc.gov.cn:8080/estimate/newtoatal?et=1&zy=001"
        yield scrapy.Request(
            url=url,
            dont_filter=True,
            callback=self.parse,
            headers=self.get_header
        )

    def parse(self, response):
        ver = response.xpath('//input[@name]/@value').extract_first("")
        # get_cookie = response.headers.getlist('Set-Cookie')[0].decode('utf-8').replace('; path=/; HttpOnly', "")

        self.page_header['__RequestVerificationToken'] = ver
        self.page_header['Cookie'] = response.res.cookies['__RequestVerificationToken'].value

        url = f"http://qycx.gzcc.gov.cn:8080/api/ToatalList/list?draw=1&columns%5B0%5D%5Bdata%5D=TotalRank&start=10&length=10&EnterpriseType=1&Specialty=001&PublishDate={datetime.datetime.now().strftime('%F')}&_={int(time.time()*1000)}"
        yield scrapy.Request(
            url=url,
            dont_filter=True,
            callback=self.deal_parse,
            headers=self.page_header
        )

    def deal_parse(self, response):
        res = json.loads(response.text)
        total_page = res["pageCount"]

        for page in range(int(total_page)):
            start = 10 * page
            url = f"http://qycx.gzcc.gov.cn:8080/api/ToatalList/list?draw=1&columns%5B0%5D%5Bdata%5D=TotalRank&start={start}&length=10&EnterpriseType=1&Specialty=001&PublishDate={datetime.datetime.now().strftime('%F')}&_={int(time.time()*1000)}"
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                callback=self.detail_parse,
                headers=self.page_header
            )

    def detail_parse(self, response):
        res = json.loads(response.text)
        trs = res["rows"]
        for tr in trs:
            tr = ezfuc.dict_to_object(tr)
            item_loader = CreditItem()
            item_loader['企业名称'] = tr.EnterpriseName
            item_loader['评价机构'] = "广州市建设工程施工和监理企业诚信评价系统"
            item_loader['行业'] = ""
            item_loader['专业'] = ""
            item_loader['信用得分'] = ""
            item_loader['信用等级'] = ""
            item_loader['排名'] = ""
            item_loader['今日得分'] = tr.TotalScore
            item_loader['今日排名'] = tr.TotalRank
            item_loader['六十日得分'] = tr.AvgScore60
            item_loader['六十日排名'] = ""
            item_loader['评价年度'] = ""
            item_loader['网站维护代码'] = "X--64"
            item_loader['发布日期'] = format_time().y_m_d
            item_loader['有效期'] = ""
            item_loader['省'] = "广东"
            item_loader['市'] = "广州"
            item_loader['网站名称'] = "广州市住房和城乡建设局施工和监理企业诚信综合评价业务信息系统"
            item_loader[
                'url'] = f"http://qycx.gzcc.gov.cn:8080/estimate/newtoataldetails?ec={tr.EnterpriseCode}&et=1&zy=001&st=010102&pd={format_time().y_m_d}&navID=2"

            yield item_loader
            # print(dict(item_loader))


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--64', 'auto', 1])
