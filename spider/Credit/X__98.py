# -*- coding: utf-8 -*-
import datetime
import scrapy
from spider_code.confs import getConfig
from spider_code.items import AutoItem, CreditItem
from fuclib import ezfuc
import manager

# configuration item
gConfig = getConfig.get_config()


class Spider(manager.Spider):
    name = 'X--98'
    headers = {
        'authority': 'xccx.z023.cn',
        'method': 'POST',
        'path': '/honestyPlatform/basecompanyinfo/ajaxListOpenZZ',
        'scheme': 'https',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://xccx.z023.cn',
        'referer': 'https://xccx.z023.cn/honestyPlatform/basecompanyinfo/openShow',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',}
    data = {
       'draw': '3',
        'columns[0][data]': 'id',
        'columns[0][name]': '',
        'columns[0][searchable]': 'false',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'companyName',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'true',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'companyUscc',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'true',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'districtCounty',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'true',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'zzName',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'true',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'totalScore',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'true',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'order[0][column]': '0',
        'order[0][dir]': 'asc',
        'start': '15',
        'length': '15',
        'search[value]': '',
        'search[regex]': 'false',
        'sort': 'id',
        'dir': 'asc',
        'companyStatusS': '5,6',
        'companyName': '',
        'companyUscc': '',
        'districtCountyCode': '3418',
        'zzCode': '',
    }
    total = 0
    url = 'https://xccx.z023.cn/honestyPlatform/basecompanyinfo/ajaxListOpenZZ'

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.data,
            headers=self.headers
        )

    def parse(self, response):
        res = response.json
        if not self.total:
            self.total = ezfuc.toal_page(res['recordsTotal'], 15)
        for i in range(self.total):
            self.data['start'] = str(15 * i)
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.data,
                callback=self.deal_parse,
                dont_filter=True,
                headers=self.headers
            )

    def deal_parse(self, response):
        res = response.json
        data = res['data']
        for i in data:
            item = CreditItem()
            item['企业名称'] = i['companyName']
            item['评价机构'] = "宣城市诚信评价系统"
            item['信用得分'] = i['totalScore']
            item['资质'] = i['zzName']
            item['网站维护代码'] = "x--98"
            item['省'] = "安徽"
            item['市'] = "宣城"
            item['网站名称'] = "宣城市住房和城乡建设局"
            item['url'] = response.url
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--98', 'auto', 1])
