# -*- coding: utf-8 -*-
import re
import time

import requests
from fuclib import ezfuc

from manager.engine import Engine
import json
from parsel import Selector
from html.parser import HTMLParser

from spider_code.confs import getConfig
from spider_code.items import CreditItem

gConfig = getConfig.get_config()

"""请求不通了跟新下data"""


class Spider(Engine):
    name = 'X--83'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.ycjsjg.net/cmis/xxfb/xypj/main.seam']
        self.url = 'http://www.ycjsjg.net/cmis/xxfb/xypj/main.seam'
        self.headers = {'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        # 'Cookie': 'JSESSIONID=506DA93AD7DF1A54704FBE242CCA7D8F.cmis_D',
                        'Host': 'www.ycjsjg.net',
                        'Origin': 'http://www.ycjsjg.net',
                        'Referer': 'http://www.ycjsjg.net/cmis/xxfb/xypj/main.seam',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',}
        self.data = 'AJAXREQUEST=_viewRoot&dtc=dtc&dtc%3Aj_id15%3Aj_id23=&dtc%3Aj_id29%3Aj_id37=-10000.0&dtc%3Aj_id29%3Aj_id39=10000.0&dtc%3Apsdtc=5&dtc%3Aj_id143=1&javax.faces.ViewState=j_id1&dtc%3Aj_id76={page}&ajaxSingle=dtc%3Aj_id76&dtc%3Aj_id77=dtc%3Aj_id77&'
        self.total = 0
        # self.proxy = True

    def before_request(self, ret):
        if ret['callback'] == 'parse':
            while 1:
                try:
                    res = requests.get(self.url, headers=self.headers)
                    break
                except:
                    print('requests请求报错。')
                    time.sleep(1)
                    continue
            ret['cookies'] = res.cookies.get_dict()
            ret['url'] = self.url + ';jsessionid=' + ret['cookies']['JSESSIONID']
        return ret

    def parse(self, response):
        page = response.meta.get('page', 1)
        if not self.total:
            total = response.xpath("//div[@class='pager']/div[@class='left']/strong[last()]/text()").extract_first().strip()
            self.total = ezfuc.toal_page(total, 5)

        content_li = response.xpath("//tbody[@id='dtc:dt_dtc:tb']/tr")
        for i in content_li:
            item = CreditItem()
            item['企业名称'] = i.xpath("./td[1]/text()").extract_first("").strip()
            item['评价机构'] = "宜昌市建筑市场信用管理平台"
            item['信用得分'] = i.xpath("./td[5]/span/text()").extract_first("").strip()
            item['信用等级'] = i.xpath("./td[4]/span/text()").extract_first("").strip()
            item['网站维护代码'] = "x--83"
            item['资质'] = i.xpath("./td[2]/text()").extract_first("").strip()
            item['省'] = "湖北"
            item['市'] = "宜昌"
            item['网站名称'] = "宜昌市住房和城乡建设局"
            item['url'] = "http://www.ycjsjg.net/cmis/xxfb/xypj/main.seam"
            self.pipeline(item)

        if page < self.total:
            page += 1
            data = self.data.format(page=str(page))
            self.produce(
                url=self.url,
                data=data,
                method='post',
                callback=self.parse,
                headers=self.headers,
                meta={'page': page}
            )


if __name__ == '__main__':
    from manager.run import run

    run(['Credit', 'X--83', 'w', 1])
