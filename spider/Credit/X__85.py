# -*- coding: utf-8 -*-
from manager.engine import Engine
import json
import time

from spider_code.confs import getConfig
from spider_code.items import CreditItem
from spider_code.api import hj_tools as eamonn

gConfig = getConfig.get_config()


class Spider(Engine):
    name = 'X--85'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.url = 'http://dn4.gxzjt.gov.cn:1181/szjsframegl/rest/frame/gxcreditevaluation/gxxypjdanweiinfo/gxxypjdanweiinfolistaction/getDataGridData2'
        self.data = {
            'pageIndex': '0',
            'pageSize': '10',
            'sortField': 'totalscore',
            'sortOrder': 'desc',
            'isSecondRequest': 'true',
            'commonDto': '[{"id":"search_entcode","bind":"dataBean.entcode","type":"textbox","value":""},{"id":"search_entname","bind":"dataBean.entname","type":"textbox","value":""},{"id":"search_enttype","bind":"dataBean.enttype","type":"radiobuttonlist","action":"enttypeModel","textField":"text","valueField":"id","value":"0"},{"id":"search_zhucearea","bind":"dataBean.zhucearea","type":"treeselect-non-nested","action":"getAreaModel","idField":"id","textField":"text","imgField":"img","iconField":"iconCls","parentField":"pid","url":"getAreaModel","valueField":"id","pinyinField":"tag","value":"","text":""},{"id":"datagrid","type":"datagrid","action":"getDataGridData2","idField":"rowguid","pageIndex":%s,"sortField":"totalscore","sortOrder":"desc","columns":[{"fieldName":"enttype","code":"企业类别"},{"fieldName":"entname"},{"fieldName":"entcode"},{"fieldName":"zhucearea"},{"fieldName":"totalscore"}],"pageSize":10,"url":"getDataGridData2","data":[],"isSecondRequest":true},{"id":"_common_hidden_viewdata","type":"hidden","value":""}]',
        }
        self.headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'dn4.gxzjt.gov.cn:1181',
            'Origin': 'http://dn4.gxzjt.gov.cn:1181',
            'Referer': 'http://dn4.gxzjt.gov.cn:1181/szjsframegl/frame/gxcreditevaluation/gxxypjdanweiinfo/gxxypjdanweiinfolist2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.proxy = True
        self.total = 0
        self.total_count = 0
        self.page = 0

    def start_requests(self):
        self.data['commonDto'] = self.data['commonDto'] % '0'
        self.produce(
            url=self.url,
            method='post',
            data=self.data,
            headers=self.headers
        )

    def parse(self, response):
        result = json.loads(response.text)
        if not self.total:
            self.total = eamonn.page(result['controls'][0]['total'], 10)
        if not self.total_count:
            self.total_count = result['controls'][0]['total']
        content_li = result['controls'][0]['data']
        for i in content_li:
            item = CreditItem()
            item['企业名称'] = i['entname']
            item['评价机构'] = "广西省建筑企业信用评价管理系统"
            item['信用得分'] = i['totalscore']
            item['网站维护代码'] = "x--85"
            item['发布日期'] = time.strftime("%F", time.localtime(int(i['updatedate']/1000)))
            item['省'] = "广西"
            item['市'] = "广西"
            item['网站名称'] = "广西建筑市场监管与诚信信息一体化平台信息发布"
            item['url'] = 'http://dn4.gxzjt.gov.cn:1181/szjsframegl/frame/gxcreditevaluation/gxxypjdanweiinfo/gxxypjdanweiinfolist2'
            self.pipeline(item)

        while self.page < self.total-1:
            self.page += 1
            self.data['pageIndex'] = str(self.page)
            self.data['commonDto'] = '[{"id":"search_entcode","bind":"dataBean.entcode","type":"textbox","value":""},{"id":"search_entname","bind":"dataBean.entname","type":"textbox","value":""},{"id":"search_enttype","bind":"dataBean.enttype","type":"radiobuttonlist","action":"enttypeModel","textField":"text","valueField":"id","value":"0"},{"id":"search_zhucearea","bind":"dataBean.zhucearea","type":"treeselect-non-nested","action":"getAreaModel","idField":"id","textField":"text","imgField":"img","iconField":"iconCls","parentField":"pid","url":"getAreaModel","valueField":"id","pinyinField":"tag","value":"","text":""},{"id":"datagrid","type":"datagrid","action":"getDataGridData2","idField":"rowguid","pageIndex":%s,"sortField":"totalscore","sortOrder":"desc","columns":[{"fieldName":"enttype","code":"企业类别"},{"fieldName":"entname"},{"fieldName":"entcode"},{"fieldName":"zhucearea"},{"fieldName":"totalscore"}],"pageSize":10,"url":"getDataGridData2","data":[],"isSecondRequest":true},{"id":"_common_hidden_viewdata","type":"hidden","value":""}]' % str(self.page)
            self.produce(
                url=self.url,
                method='post',
                data=self.data,
                headers=self.headers,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        result = json.loads(response.text)
        content_li = result['controls'][0]['data']
        for i in content_li:
            item = CreditItem()
            item['企业名称'] = i['entname']
            item['评价机构'] = "广西省建筑企业信用评价管理系统"
            item['信用得分'] = i['totalscore']
            item['网站维护代码'] = "x--85"
            item['发布日期'] = time.strftime("%F", time.localtime(int(i['updatedate']/1000)))
            item['省'] = "广西"
            item['市'] = "广西"
            item['网站名称'] = "广西建筑市场监管与诚信信息一体化平台信息发布"
            item['url'] = 'http://dn4.gxzjt.gov.cn:1181/szjsframegl/frame/gxcreditevaluation/gxxypjdanweiinfo/gxxypjdanweiinfolist2'
            self.pipeline(item)


if __name__ == '__main__':
    from manager.run import run

    run(['Credit', 'X--85', 'auto', 1])
