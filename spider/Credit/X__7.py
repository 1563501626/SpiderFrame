# -*- coding: utf-8 -*-
from manager.engine import Engine
import json
from fuclib import ezfuc

from spider_code.confs import getConfig
from urllib.parse import quote

from spider_code.items import CreditItem

gConfig = getConfig.get_config()


class Spider(Engine):
    name = 'X--7'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        # self.filter_data = True
        self.get_header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': '202.61.88.188',
            'Referer': 'http://202.61.88.188/xmgk/loyall/Loyal.aspx',
            'Cookie': 'Hm_lvt_6647b45850e12bf42ce7ed42bd381746=1593996069,1594620923; Hm_lpvt_6647b45850e12bf42ce7ed42bd381746=1594711152',
            'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.116Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.url = 'http://202.61.88.188/xmgk/api/getdata/GetLoyalList?id=%7B%22sd%22%3A%22%22%2C%22lb%22%3A%22%22%2C%22mc%22%3A%22{name}%22%2C%22bh%22%3A%22%22%2C%22kcsj%22%3A%22%22%2C%22itype%22%3A%22%22%2C%22validate%22%3A%22%22%7D'
        self.db = getConfig.company_name_db()
        self.custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'spider_code.middlewares.ProxyMiddleware': 543,
                # 'spider_code.middlewares.SpiderCodeDownloaderMiddleware': 542,
            },
            'DOWNLOAD_TIMEOUT': 240
        }
        # self.proxy = True
        self.timeout = 240

    def start_requests(self):
        companies = self.db.query("select company_name from company_name_copy where IsLock_Creadit=1")
        # companies = self.db.query("select company_name from company_name_copy where updated>='2020-09-04'")
        for company in companies:
            url = self.url.format(name=quote(company['company_name']))
            self.produce(
                url=url,
                headers=self.get_header,
            )

    def before_request(self, ret):
        ret['proxies'] = None
        return ret

    def parse(self, response):
        try:
            result = json.loads(response.text)
        except:
            self.produce(
                url=response.url,
                headers=self.get_header,
            )
            return
        if result:
            for i in result:
                Score = i['zf']
                企业名称 = i['QYMC']
                评价机构 = "四川省住房和诚信行业信用分"
                行业 = ''
                专业 = i['qylxmc']
                信用得分 = Score
                信用等级 = ''
                排名 = ""
                今日得分 = ''
                今日排名 = ''
                六十得分 = ''
                六十日排名 = ''
                评价年度 = ""
                网站维护代码 = "X--7"
                发布日期 = ''
                有效期 = ""
                省 = "四川"
                市 = "四川"
                网站名称 = "四川省住房和城乡建设行业数据共享平台"
                url = f"http://jst.sc.gov.cn/xxgx/Enterprise/eBlxx.aspx?id={i['QYBM']}"
                # encode_md5 = ezfuc.md5(网站名称, 企业名称, str(信用得分), 行业, url, 3)
                item = CreditItem()
                item['企业名称'] = 企业名称
                item['评价机构'] = 评价机构
                item['行业'] = 行业
                item['专业'] = 专业
                item['信用得分'] = 信用得分
                item['信用等级'] = 信用等级
                item['排名'] = 排名
                item['今日得分'] = 今日得分
                item['今日排名'] = 今日排名
                item['六十日得分'] = 六十得分
                item['六十日排名'] = 六十日排名
                item['评价年度'] = 评价年度
                item['网站维护代码'] = 网站维护代码
                item['发布日期'] = 发布日期
                item['有效期'] = 有效期
                item['省'] = 省
                item['市'] = 市
                item['网站名称'] = 网站名称
                item['url'] = "'"+url+"'"
                # item['md5'] = encode_md5
                self.pipeline(item)
            # self.db.query("update company_name_copy set IsLock_Creadit=1 where company_name='%s'" % item["企业名称"])
            # print(item['企业名称'])


if __name__ == '__main__':
    from manager.run import run

    run(["Credit", 'X--7', "w", 3])
