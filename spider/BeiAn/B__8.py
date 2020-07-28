# -*- coding: utf-8 -*-
from manager.engine import Engine
from confs import getConfig
from items import BeianItem
from fuclib import ezfuc

# configuration item
gConfig = getConfig.get_config()


class Spider(Engine):
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.name = 'B--8'
        self.post_header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'zh-CN,zh;q=0.9',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Host': 'jgpt.lnzb.cn',
                            'Origin': 'http://jgpt.lnzb.cn',
                            'Referer': 'http://jgpt.lnzb.cn/qyxx/004002/about_ztxx.html?categorynum=004002',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                          '(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-Real-IP': '192.168.0.116',
                            'X-Forwarded-For': '192.168.0.116'
                            }

        self.post_data = {'danweiname': '',
                          'pageindex': '1',
                          'pagesize': '12',
                          'type': '13',
                          'unitorgnum': '',
                          'zizhicode': ''}

    def start_requests(self):
        url = 'http://jgpt.lnzb.cn/EpointWebBuilder_ln/getZtxxInfoAction.action?cmd=getZtxxInfo'
        self.produce(
            method='post',
            url=url,
            headers=self.post_header,
            data=self.post_data
        )

    def parse(self, response):
        res = ezfuc.dict_to_object(response.text)

        total = ezfuc.dict_to_object(res.custom).EpointDataBody.COUNT

        total_page = ezfuc.toal_page(total, 12)
        for page in range(total_page):
            self.post_data['pageindex'] = str(page)
            self.produce(
                method='post',
                url=response.url,
                headers=self.post_header,
                data=self.post_data,
                callback=self.deal_parse
            )

    def deal_parse(self, response):
        res = ezfuc.dict_to_object(response.text)

        trs = ezfuc.dict_to_object(res.custom).EpointDataBody.DATA.UserArea
        trs = ezfuc.dict_to_object(trs)
        for tr in trs:
            item_model = BeianItem()
            item_model["企业名称"] = tr.danweiname
            item_model["企业链接地址"] = tr.url
            # item_model["企业类型"] = tr.
            # item_model["企业营业地址"] = tr.
            # item_model["所属地区"] = tr.
            item_model["采集来源省"] = "辽宁省"
            item_model["省内或省外"] = "省外"
            item_model["来源网站"] = "辽宁建设工程网"
            item_model["网站代码"] = "B--8"
            self.pipeline(item_model)
            # yield item_model


if __name__ == '__main__':
    from manager.run import run

    run(["spider/BeiAn/B__8.py", "w", 1])
