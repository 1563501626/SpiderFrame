# -*- coding: utf-8 -*-
import scrapy
import re,json
import datetime
import pymssql,random
from urllib.parse import quote


import manager
class Spider(manager.Spider):
    name = 'sichuan'
    allowed_domains = ['http://jst.sc.gov.cn']
    start_urls = ['http://jst.sc.gov.cn/xmgk/loyall/Loyal.aspx']
    custom_settings = {
        "ITEM_PIPELINES": {
            # "XinYongpj_Spider.pipelines.TuniuPipeline":300,
            "XinYongpj_Spider.pipelines.ServerPipeline": 301
        }
    }
    post_data = {
        "qylx": "",
        "xydm": "",
        "fr": "",
        "zsbh": "",
        "ctl00$MainContent$Button1": "搜索"
    }
    post_headers = {
        "Host":"jst.sc.gov.cn",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding":"gzip, deflate",
        "Referer":"http://jst.sc.gov.cn/xxgx/loyall/Loyal.aspx",
        "Content-Type":"application/x-www-form-urlencoded",
        "Connection":"keep-alive"
    }
    get_header = {
        "Host": "jst.sc.gov.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://jst.sc.gov.cn/xxgx/loyall/Loyal.aspx",
        "Connection": "keep-alive",
        "X-Requested-With":"XMLHttpRequest",
        "Pragma":"no-cache",
        "Cache-Control":"no-cache"
    }
    def start_requests(self):
        # sql = "select Company_name,CID from SDH_Company where IsLock_Creadit=0 order by NEWID()"
        sql = "select Company_name,CID from SDH_Company"
        with pymssql.connect(host=Dao.host, user=Dao.user, password=Dao.password, database=database, charset="utf8") as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                resList = cursor.fetchall()
        if len(resList):
            for mc in resList:
                # self.get_header['X-Forwarded-For'] = f"{random.randint(1, 200)}.{random.randint(1, 200)}.{random.randint(1, 200)}.{random.randint(1, 200)}"
                self.get_header['X-Real-IP'] = f"{random.randint(1, 200)}.{random.randint(1, 200)}.{random.randint(1, 200)}.{random.randint(1, 200)}"
                Company_name = mc[0]
                CID = mc[1]
                # parm = '{"sd":"","lb":"","mc":"%s","bh":"","kcsj":"","itype":"","validate":""}'%Company_name
                # url = f'http://jst.sc.gov.cn/xmgk/api/getdata/GetLoyalList?id={quote(parm)}'
                url = 'http://jst.sc.gov.cn/xxgx/api/getdata/GetLoyalList?id={"sd":"","lb":"","mc":"%s","bh":"","kcsj":"","itype":"","validate":""}'%Company_name
                yield scrapy.Request(
                    url=url,
                    meta={"CID":CID},
                    headers=self.get_header,
                    dont_filter=True
                )

    def parse(self, response):
        result = json.loads(response.text)
        if result:
            for i in result:
                Score = i['zf']
                if Score != 0:
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
                    encode_md5 = Md5(网站名称 + 企业名称 + str(信用得分) + 行业 + url)
                    item = XingYong()
                    item['企业名称'] = 企业名称
                    item['评价机构'] = 评价机构
                    item['行业'] = 行业
                    item['专业'] = 专业
                    item['信用得分'] = 信用得分
                    item['信用等级'] = 信用等级
                    item['排名'] = 排名
                    item['今日得分'] = 今日得分
                    item['今日排名'] = 今日排名
                    item['六十得分'] = 六十得分
                    item['六十日排名'] = 六十日排名
                    item['评价年度'] = 评价年度
                    item['网站维护代码'] = 网站维护代码
                    item['发布日期'] = 发布日期
                    item['有效期'] = 有效期
                    item['省'] = 省
                    item['市'] = 市
                    item['网站名称'] = 网站名称
                    item['url'] = url
                    item['data_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    item['encode_md5'] = encode_md5
                    item['update_code'] = "0"
                    yield item
            sql = "update SDH_Company set IsLock_Creadit=1 where CID=%s" % response.meta['CID']
            with pymssql.connect(host=Dao.host, user=Dao.user, password=Dao.password, database=database,
                                 charset="utf8") as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    conn.commit()
        else:
            sql = "update SDH_Company set IsLock_Creadit=1 where CID=%s" % response.meta['CID']
            with pymssql.connect(host=Dao.host, user=Dao.user, password=Dao.password, database=database,
                                 charset="utf8") as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    conn.commit()




