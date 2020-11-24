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
    name = 'X--102'
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
        'commonDto': r'[{"id":"unitorgnum","bind":"unitorgnum","type":"textbox","value":"","text":""},{"id":"danweiname","bind":"danweiname","type":"textbox","value":"","text":""},{"id":"hangyefenleichild","bind":"hangyefenleichild","type":"combobox","action":"SelectModel","textField":"text","valueField":"id","pinyinField":"tag","columns":[],"value":"01","text":"施工"},{"id":"datagrid","type":"datagrid","action":"getDataGridData","idField":"rowguid","pageIndex":%s,"pageSize":15,"sortField":"","sortOrder":"","columns":[{"fieldName":"unitorgnum"},{"fieldName":"danweiname"},{"fieldName":"finalscore"},{"fieldName":"cxnum"},{"fieldName":"xzjdscore"},{"fieldName":"hyzgscore"},{"fieldName":"zbrscore"},{"fieldName":"qtdwscore"}],"url":"UnitsTodayNumListAction.action?cmd=getDataGridData","data":[],"isSecondRequest":true},{"id":"_common_hidden_viewdata","type":"hidden","value":"{\"HangYeFenLei\":\"01\"}"}]',

    }
    # data = 'pageIndex=0&pageSize=15&sortField=&sortOrder=&isSecondRequest=true&commonDto=%5B%7B%22id%22%3A%22unitorgnum%22%2C%22bind%22%3A%22unitorgnum%22%2C%22type%22%3A%22textbox%22%2C%22value%22%3A%22%22%2C%22text%22%3A%22%22%7D%2C%7B%22id%22%3A%22danweiname%22%2C%22bind%22%3A%22danweiname%22%2C%22type%22%3A%22textbox%22%2C%22value%22%3A%22%22%2C%22text%22%3A%22%22%7D%2C%7B%22id%22%3A%22hangyefenleichild%22%2C%22bind%22%3A%22hangyefenleichild%22%2C%22type%22%3A%22combobox%22%2C%22action%22%3A%22SelectModel%22%2C%22textField%22%3A%22text%22%2C%22valueField%22%3A%22id%22%2C%22pinyinField%22%3A%22tag%22%2C%22columns%22%3A%5B%5D%2C%22value%22%3A%2201%22%2C%22text%22%3A%22%E6%96%BD%E5%B7%A5%22%7D%2C%7B%22id%22%3A%22datagrid%22%2C%22type%22%3A%22datagrid%22%2C%22action%22%3A%22getDataGridData%22%2C%22idField%22%3A%22rowguid%22%2C%22pageIndex%20%3A0%2C%22pageSize%22%3A15%2C%22sortField%22%3A%22%22%2C%22sortOrder%22%3A%22%22%2C%22columns%22%3A%5B%7B%22fieldName%22%3A%22unitorgnum%22%7D%2C%7B%22fieldName%22%3A%22danweiname%22%7D%2C%7B%22fieldName%22%3A%22finalscore%22%7D%2C%7B%22fieldName%22%3A%22cxnum%22%7D%2C%7B%22fieldName%22%3A%22xzjdscore%22%7D%2C%7B%22fieldName%22%3A%22hyzgscore%22%7D%2C%7B%22fieldName%22%3A%22zbrscore%22%7D%2C%7B%22fieldName%22%3A%22qtdwscore%22%7D%5D%2C%22url%22%3A%22UnitsTodayNumListAction.action%3Fcmd%3DgetDataGridData%22%2C%22data%22%3A%5B%5D%2C%22isSecondRequest%22%3Atrue%7D%2C%7B%22id%22%3A%22_common_hidden_viewdata%22%2C%22type%22%3A%22hidden%22%2C%22value%22%3A%22%7B%5C%22HangYeFenLei%5C%22%3A%5C%2201%5C%22%7D%22%7D%5D'
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
            item['网站维护代码'] = "x--102"
            item['省'] = "安徽"
            item['市'] = "芜湖"
            item['网站名称'] = "芜湖市公共资源交易中心"
            item['url'] = 'http://whsggzy.wuhu.gov.cn/cxpj/008001/cxpj1.html'
            yield item


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--102', 'auto', 1])
