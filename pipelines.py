# -*- coding: utf-8 -*-
from fuclib import MySql
from fuclib import ezfuc
import config


class BeiAnPipeline(object):

    def __init__(self):
        self.host = config.sql_host
        self.username = config.sql_user
        self.password = config.sql_pwd
        self.database = "zlcollector_beian"
        self.port = 3306
        self.db = MySql(self.host, self.database, self.username, self.password, self.port)
        self.db1 = MySql(self.host, "company", self.username, self.password, self.port)

    def open_spider(self, spider):
        if hasattr(spider, "filter_data") and spider.filter_data:
            attr = ["filter_db", "filter_table"]
            for i in attr:
                if not hasattr(spider, i):
                    raise Exception("数据去重配置未完善.")
            spider.filter_conn = MySql(self.host, spider.filter_db, self.username, self.password, self.port)

    def process_item(self, item, spider):
        items = dict(item)
        if hasattr(spider, "filter_data") and spider.filter_data:
            md5 = items['md5']
            items.pop('md5')
            rest = spider.filter_conn.get("select md5 from %s where md5='%s'" % (spider.filter_table, md5))
            if not rest:
                items['spider_name'] = spider.name
                self.db.insert('beian_all', items)
                spider.filter_conn.insert(spider.filter_table, {"md5": md5})
                aa = items
            else:
                aa = "数据重复，已过滤."
        else:
            items['spider_name'] = spider.name
            # self.db.insert('beian_all', items)
            aa = items
        company_name = items["企业名称"]
        company_name_md5 = ezfuc.md5(company_name)
        ret = self.db1.get("select md5 from company_md5 where md5='%s'" % company_name_md5)
        if not ret:
            self.db1.insert("company_name", {"企业名称": company_name})
            self.db1.insert("company_md5", {"md5": company_name_md5})
        return aa

    def close_spider(self, spider):
        self.db.close()
        self.db1.close()
        if hasattr(spider, "filter_data") and spider.filter_data:
            spider.filter_conn.close()
