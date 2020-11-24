# -*- coding: utf-8 -*-
import re

from manager.engine import Engine
import datetime
from spider_code.api import hj_tools as eamonn
from spider_code.confs import getConfig
from spider_code.items import AutoItem

gConfig = getConfig.get_config()


class Spider(Engine):
    name = 'X--89'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://cxtx.stjs.org.cn/Estimate/OA/MainQueryMarkZZ.aspx?clearPaging=true']
        self.url = 'http://cxtx.stjs.org.cn/Estimate/OA/MainQueryMarkZZ.aspx?clearPaging=true'
        self.headers = {'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Host': 'cxtx.stjs.org.cn',
                        'Origin': 'http://cxtx.stjs.org.cn',
                        'Referer': 'http://cxtx.stjs.org.cn/Estimate/OA/MainQueryMarkZZ.aspx?clearPaging=true',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                        'X-MicrosoftAjax': 'Delta=true',
                        'X-Requested-With': 'XMLHttpRequest',}
        self.data = {
            'ctl00$ScriptManager2': 'ctl00$UpdatePanel1|ctl00$cph_content$GridViewPaging1$btnForwardToPage',
            'ctl00$WidthPixel': '',
            'ctl00$HeightPixel': '',
            'ctl00$cph_content$drpTitle': '9',
            'ctl00$cph_content$txtEnterName': '',
            'ctl00$cph_content$txtDay': datetime.datetime.now().strftime("%F"),
            'ctl00$cph_content$GridViewPaging1$txtGridViewPagingForwardTo': '3',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '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',
            '__VIEWSTATEENCRYPTED': '',
            '__EVENTVALIDATION': 'AQ0oyIikLJZY3zDY8zuovV69ngKinKkPpYPLm9igB0W9GrNXhAcmGFO30QDPLakNkhQ/h5kI73kRvhfcvnDdfcVzgsXA3tIz2gVch/0TH85puhysuR4FYIxmWdcAjvufSN+JxwuYBRrqCKFlgpSZKKMyvCLN7PJKdjMhLywQCf0=',
            '__ASYNCPOST': 'true',
            'ctl00$cph_content$GridViewPaging1$btnForwardToPage': 'Go',
        }
        self.total = 0
        self.total_count = 0
        self.page = 1

    def parse(self, response):
        if not self.total:
            self.total = eamonn.page(int(re.search(r"共<.*?>(\d+)<.*?>条数据", response.text).group(1)), 20)
        if not self.total_count:
            self.total_count = re.search(r"共<.*?>(\d+)<.*?>条数据", response.text).group(1)
        content_li = response.xpath("//table[@class='gridviewStyle']/tr")[1:]
        for i in content_li:
            item = AutoItem()
            item['企业名称'] = i.xpath("./td[3]/text()").extract_first("").strip()
            item['总排名'] = i.xpath("./td[1]/span/text()").extract_first("").strip()
            item['等级排名'] = i.xpath("./td[2]/text()").extract_first("").strip()
            item['市场行为'] = i.xpath("./td[4]/text()").extract_first("").strip()
            item['质量安全'] = i.xpath("./td[5]/text()").extract_first("").strip()
            item['其他'] = i.xpath("./td[6]/text()").extract_first("").strip()
            item['信用得分'] = i.xpath("./td[7]/span/text()").extract_first("").strip()
            item['发布日期'] = i.xpath("./td[8]/text()").extract_first("").strip()
            item['评价类别'] = i.xpath("./td[9]/text()").extract_first("").strip()
            item['评价机构'] = "汕头市施工企业诚信综合评价体系"
            item['网站维护代码'] = "x--89"
            item['省'] = "广东"
            item['市'] = "汕头"
            item['网站名称'] = "汕头市建设局（汕头市施工企业诚信综合评价体系）"
            item['url'] = self.url
            self.pipeline(item)

        while self.page < self.total:
            self.page += 1
            self.data['ctl00$cph_content$GridViewPaging1$txtGridViewPagingForwardTo'] = str(self.page)
            self.data['__VIEWSTATE'] = response.xpath("//input[@name='__VIEWSTATE']/@value").extract_first("").strip()
            self.data['__EVENTVALIDATION'] = response.xpath("//input[@name='__EVENTVALIDATION']/@value").extract_first("").strip()
            self.produce(
                url=self.url,
                method='post',
                data=self.data,
                headers=self.headers,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        content_li = response.xpath("//table[@class='gridviewStyle']/tr")[1:]
        for i in content_li:
            item = AutoItem()
            item['企业名称'] = i.xpath("./td[3]/text()").extract_first("").strip()
            item['总排名'] = i.xpath("./td[1]/span/text()").extract_first("").strip()
            item['等级排名'] = i.xpath("./td[2]/text()").extract_first("").strip()
            item['市场行为'] = i.xpath("./td[4]/text()").extract_first("").strip()
            item['质量安全'] = i.xpath("./td[5]/text()").extract_first("").strip()
            item['其他'] = i.xpath("./td[6]/text()").extract_first("").strip()
            item['信用得分'] = i.xpath("./td[7]/span/text()").extract_first("").strip()
            item['发布日期'] = i.xpath("./td[8]/text()").extract_first("").strip()
            item['评价类别'] = i.xpath("./td[9]/text()").extract_first("").strip()
            item['评价机构'] = "汕头市施工企业诚信综合评价体系"
            item['网站维护代码'] = "x--89"
            item['省'] = "广东"
            item['市'] = "汕头"
            item['网站名称'] = "汕头市建设局（汕头市施工企业诚信综合评价体系）"
            item['url'] = self.url
            self.pipeline(item)


if __name__ == '__main__':
    from manager.run import run

    run(['Credit', 'X--89', 'auto', 1])