# -*- coding: utf-8 -*-
from spider import Engine, selector
import time
import json


class Spider(Engine):
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.allow_status_code = [404]
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

    def start_request(self):
        for i in range(1, 10):
            url = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=7&tenderkind=All&projecttendersite=SS&orderFiled=fcInfostartdate&orderValue=desc'
            data = {
                'fcInfotitle': '',
                'currentPage': '{}'.format(i),
            }
            self.produce(url, method='post', data=data, headers=self.headers)

    def parse(self, res):
        ret = json.loads(res.text)
        content_li = ret["ls"]
        for i in content_li:
            title = i["fcInfotitle"]
            issuetime = i["fcInfostartdate"]
            fcInfotype = i['fcInfotype']
            nextid = i['id']
            meta = {'title':title, 'issuetime':issuetime}
            url = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/jsdetail?publishId={}&fcInfotype={}'.format(nextid, fcInfotype)
            self.produce(url, headers=self.headers, callback='parse_detail', meta=meta)

    def parse_detail(self, res):
        ret = selector(res)
        content = ret.xpath("string(//div[@class='content'])").extract_first()
        title = res.meta['title']
        issuetime = res.meta['issuetime']
        bidtype = 0
        if not content:
            print('no content')
            return
        if not title:
            title = 'no title'
        datasource = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/jslist?fcInfotype=7&TypeIndex=2&KindIndex=-1'
        if not issuetime:
            print('no issuetime')
        url = res.url
        if not url:
            print('no url')
        id = time.time()
        region = '东莞市公共资源交易'

        print("****************************************************")
        item = ['id', 'title', 'bidtype', 'region', 'issuetime', 'datasource', 'url']
        value = [id, title, bidtype, region, issuetime, datasource, url]
        print(dict(zip(item, value)))