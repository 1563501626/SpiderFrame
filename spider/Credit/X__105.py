# -*- coding: utf-8 -*-
import copy
import scrapy
from spider_code.confs import getConfig
from spider_code.items import AutoItem, CreditItem
from fuclib import ezfuc
import manager

# configuration item
gConfig = getConfig.get_config()


class Spider(manager.Spider):
    name = 'X--105'
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'whsggzy.wuhu.gov.cn',
        'Origin': 'http://whsggzy.wuhu.gov.cn',
        'Referer': 'http://whsggzy.wuhu.gov.cn/TPBidder/chengxinmark/cxglztbmis/pages/wangzhanshowcxnum/Units_List?HangYeFenLei=01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',}
    data = {
       'pageIndex': '0',
        'pageSize': '15',
        'sortField': '',
        'sortOrder': '',
        'isSecondRequest': 'true',
        'commonDto': r'[{"id":"unitorgnum","bind":"unitorgnum","type":"textbox","value":"","text":""},{"id":"danweiname","bind":"danweiname","type":"textbox","value":"","text":""},{"id":"hangyefenleichild","bind":"hangyefenleichild","type":"combobox","action":"SelectModel","textField":"text","valueField":"id","pinyinField":"tag","columns":[],"value":"01","text":"施工"},{"id":"datagrid","type":"datagrid","action":"getDataGridData","idField":"rowguid","pageIndex":%s,"pageSize":15,"sortField":"","sortOrder":"","columns":[{"fieldName":"unitorgnum"},{"fieldName":"danweiname"},{"fieldName":"finalscore"},{"fieldName":"cxnum"},{"fieldName":"xzjdscore"},{"fieldName":"hyzgscore"},{"fieldName":"zbrscore"},{"fieldName":"qtdwscore"}],"url":"UnitsTodayNumListAction.action?cmd=getDataGridData","data":[],"isSecondRequest":true},{"id":"_common_hidden_viewdata","type":"hidden","value":"{\"HangYeFenLei\":\"03\"}"}]',

    }
    total = 0
    cookie = {}
    url = 'http://whsggzy.wuhu.gov.cn/TPBidder/chengxinmark/cxglztbmis/pages/wangzhanshowcxnum/UnitsTodayNumListAction.action?cmd=getDataGridData'

    def format_data(self, page):
        data = copy.deepcopy(self.data)
        data['pageIndex'] = str(page)
        data['commonDto'] = data['commonDto'] % str(page)
        return data

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.format_data(0),
            headers=self.headers,
        )

    def parse(self, response):
        res = response.json
        if not self.total:
            self.total = ezfuc.toal_page(res['controls'][0]['total'], 15)
        for i in range(self.total):
            yield scrapy.FormRequest(
                url=self.url,
                formdata=self.format_data(i),
                callback=self.deal_parse,
                dont_filter=True,
                headers=self.headers
            )

    def deal_parse(self, response):
        res = response.json
        data = res['controls'][0]['data']
        for i in data:
            item = CreditItem()
            item['企业名称'] = i['danweiname']
            item['评价机构'] = "芜湖市公共资源交易诚信评价信息系统"
            item['信用得分'] = i['finalscore']
            item['网站维护代码'] = "x--105"
            item['省'] = "安徽"
            item['市'] = "芜湖"
            item['网站名称'] = "芜湖市公共资源交易中心"
            item['url'] = 'http://whsggzy.wuhu.gov.cn/cxpj/008001/cxpj1.html'
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--105', 'auto', 1])
