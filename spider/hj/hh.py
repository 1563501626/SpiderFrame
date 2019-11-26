# -*- coding: utf-8 -*-
from spider import Engine, selector
import time
import json


class Spider(Engine):
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.allow_status_code = [404]
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        self.auto_frequency = 0.01
        self.count = 0
        self.count1 = 0

    def start_request(self):
        for i in range(1, 5):
            url = 'http://portal.gd-n-tax.gov.cn/siteapps/webpage/gdtax/zdgkml/xxgkml_list.jsp'
            data = {
                'websiteId':'8676232ec118450ba0eff07aa583b54c',
                'maxPage':'83',
                'title':'',
                'c_syh':'',
                'tc_name':'',
                'pagination_input': i,
            }
            self.produce(url, method='post', data=data, headers=self.headers)
            # url = 'https://www.baidu.com'
            # self.produce(url, callback='parse_detail')

    def parse(self, res):
        # ret = selector(res.text)
        # li = ret.xpath("//tbody[@id='documentContainer']//a/@href").extract()
        # for i in li:
        url = 'https://baidu.com'

        self.produce(url, headers=self.headers, callback='parse_detail')
        # self.count1 += 1
        # print('parse:'+str(res.status_code), self.count1)

    def parse_detail(self, res):
        # ret = selector(res)
        # content = ret.xpath("string(//div[@class='content'])").extract_first()
        # title = ret.xpath("string(//div[@class='title'])").extract_first()
        # issuetime = ret.xpath("//span//a/@href").extract_first()
        # bidtype = 0
        # if not content:
        #     print('no content')
        #     return
        # if not title:
        #     title = 'no title'
        # datasource = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/jslist?fcInfotype=7&TypeIndex=2&KindIndex=-1'
        # if not issuetime:
        #     print('no issuetime')
        # url = res.url
        # if not url:
        #     print('no url')
        # id = time.time()
        # region = '东莞市公共资源交易'
        #
        # print("****************************************************")
        # item = ['id', 'title', 'bidtype', 'region', 'issuetime', 'datasource', 'url']
        # value = [id, title, bidtype, region, issuetime, datasource, url]
        # print(dict(zip(item, value)))
        # self.count += 1
        # print("parse_detail" + str(res.status_code), self.count)
        # time.sleep(0.0001)
        # self.produce(res.url)
        print(res.status_code)
        # print(self.db.select_sql("mytest", 'name'))
