# -*- coding: utf-8 -*-
import scrapy
import re
from spider_code.api import hj_tools as eamonn
from spider_code.confs import getConfig
from spider_code.items import CreditItem
from fuclib import ezfuc

# configuration item
gConfig = getConfig.get_config()


import manager
class X73Spider(manager.Spider):
    name = 'X--73'
    download_delay = float(gConfig.sleep_time)

    def __init__(self, *args, **kwargs):
        super(X73Spider, self).__init__(*args, **kwargs)
        # self.start_urls = ["http://219.131.222.110:8899/cbms/score/cbmsEntCreditInterfaceAction!toZhcx.action"]
        self.post_header = ezfuc.struct_header("""POST /cbms/score/cbmsEntCreditInterfaceAction!toZhcx.action HTTP/1.1
                                Host: 219.131.222.110:8899
                                Connection: keep-alive
                                Cache-Control: max-age=0
                                Origin: http://219.131.222.110:8899
                                Upgrade-Insecure-Requests: 1
                                Content-Type: application/x-www-form-urlencoded
                                User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36
                                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                                Referer: http://219.131.222.110:8899/cbms/score/cbmsEntCreditInterfaceAction!toZhcx.action
                                Accept-Encoding: gzip, deflate
                                Accept-Language: zh-CN,zh;q=0.9""")
        self.post_data = ezfuc.struct_data(
            "evaluation.entType=9&evalpage=2&evaluation.entName=&evaluation.dfStart=&evaluation.dfend=")

    def start_requests(self):
        url = "http://219.131.222.110:8899/cbms/score/cbmsEntCreditInterfaceAction!toZhcx.action"
        yield scrapy.FormRequest(
            url=url,
            dont_filter=True,
            callback=self.parse,
            headers=self.post_header,
            formdata=self.post_data
        )

    def parse(self, response):
        total_pages = response.css('.pagination>li:last-child>a::attr(onclick)').extract_first("")
        _, total_pages = eamonn.ex(total_pages, ["re", "'(.*?)'"])
        for page in range(1, int(total_pages) + 1):
            self.post_data['evalpage'] = str(page)
            yield scrapy.FormRequest(
                url=response.url,
                dont_filter=True,
                callback=self.deal_parse,
                headers=self.post_header,
                formdata=self.post_data
            )

    def deal_parse(self, response):
        trs = response.css('.odd')
        for tr in trs:
            onclick = tr.css('td:nth-child(2)>a::attr(onclick)').extract_first("")  # onclick
            _, res = eamonn.ex(onclick.replace("'", ""), ['re', "\((.*?)\)"])
            detail_list = res.split(",")
            item_loader = CreditItem()
            item_loader['企业名称'] = tr.css('td:nth-child(2)>a::text').extract_first("")
            item_loader['评价机构'] = "珠海市建筑企业信用评价系统"
            item_loader['行业'] = ""
            item_loader['专业'] = ""
            item_loader['信用得分'] = tr.css('td:nth-last-child(2)>span::text').extract_first("")
            item_loader['信用等级'] = tr.css('td:nth-last-child(5)>span::text').extract_first("")
            item_loader['排名'] = tr.css('td:nth-child(1)::text').extract_first("")
            item_loader['今日得分'] = ""
            item_loader['今日排名'] = ""
            item_loader['六十日得分'] = tr.css('td:nth-last-child(3)>span::text').extract_first("")
            item_loader['六十日排名'] = ""
            item_loader['评价年度'] = ""
            item_loader['网站维护代码'] = "X--73"
            item_loader['发布日期'] = ""
            item_loader['有效期'] = ""
            item_loader['省'] = "广东"
            item_loader['市'] = "珠海"
            item_loader['网站名称'] = "珠海市建筑业企业信用评价信息发布平台"
            item_loader[
                'url'] = f"http://219.131.222.110:8899/cbms/score/cbmsEntCreditInterfaceAction!toXq.action?entId={detail_list[0]}&pj={detail_list[1]}&hz60={detail_list[2]}&ts={detail_list[3]}"

            yield item_loader
            # print(item_loader)


if __name__ == '__main__':
    from manager import run

    run(['Credit', 'X--73', 'auto', 1])
