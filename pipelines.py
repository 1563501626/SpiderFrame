# -*- coding: utf-8 -*-
import datetime

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
        self.count = 0
        self.db = MySql(self.host, self.database, self.username, self.password, self.port)
        self.db1 = MySql(self.host, "company", self.username, self.password, self.port)

    def open_spider(self, spider):
        if hasattr(spider, "filter_data") and spider.filter_data:
            if not hasattr(spider, "filter_db"):
                setattr(spider, "filter_db", "duplicate_key")
            if not hasattr(spider, "filter_table"):
                setattr(spider, "filter_table", "beian_%s" % spider.name.replace("-", "_"))
            spider.filter_conn = MySql(self.host, spider.filter_db, self.username, self.password, self.port)

    def process_item(self, item, spider):
        items = dict(item)
        if hasattr(spider, "filter_data") and spider.filter_data:
            md5 = items['md5']
            items.pop('md5')
            rest = spider.filter_conn.get("select `md5` from %s where md5='%s'" % (spider.filter_table, md5))
            if not rest:
                items['spider_name'] = spider.name
                self.db.insert('beian_all', items)
                spider.filter_conn.insert(spider.filter_table, {"md5": md5})
                aa = items
                self.count += 1
            else:
                aa = "数据重复，已过滤."
        else:
            items['spider_name'] = spider.name
            self.db.insert('beian_all', items)
            aa = items
            self.count += 1
        company_name = items["企业名称"]
        company_name_md5 = ezfuc.md5(company_name)
        ret = self.db1.get("select md5 from company_md5 where md5='%s'" % company_name_md5)
        if not ret:
            pass
            self.db1.insert("company_name", {"企业名称": company_name})
            self.db1.insert("company_md5", {"md5": company_name_md5})

        return aa

    def close_spider(self, spider):
        if spider.way != 'm':
            if hasattr(spider, "total_count"):
                names = ('update_time', 'total_count', 'crawl_count')
                values = (str(datetime.datetime.now()), spider.total_count, self.count)
                spider.spider_db.update_spider_info(names, values, spider.queue_name)
            else:
                names = ('update_time', 'crawl_count')
                values = (str(datetime.datetime.now()), self.count)
                spider.spider_db.update_spider_info(names, values, spider.queue_name)
        self.db.close()
        self.db1.close()
        if hasattr(spider, "filter_data") and spider.filter_data:
            spider.filter_conn.close()


class AptPipeline(object):

    def __init__(self):
        self.host = config.sql_host
        self.username = config.sql_user
        self.password = config.sql_pwd
        self.database = "zlcollector_apt"
        self.port = 3306
        self.db = MySql(self.host, self.database, self.username, self.password, self.port)
        self.db1 = MySql(self.host, "company", self.username, self.password, self.port)
        self.count = 0

    def open_spider(self, spider):
        if hasattr(spider, "filter_data") and spider.filter_data:
            if not hasattr(spider, "filter_db"):
                setattr(spider, "filter_db", "duplicate_key")
            if not hasattr(spider, "filter_table"):
                setattr(spider, "filter_table", "Apt_%s" % spider.name.replace("-", "_"))
            spider.filter_conn = MySql(self.host, spider.filter_db, self.username, self.password, self.port)

    def process_item(self, item, spider):
        items = dict(item)
        if hasattr(spider, "filter_data") and spider.filter_data:
            md5 = items['md5']
            items.pop('md5')
            rest = spider.filter_conn.get("select md5 from %s where md5='%s'" % (spider.filter_table, md5))
            if not rest:
                self.db.insert(spider.name.replace("-", '_'), items)
                spider.filter_conn.insert(spider.filter_table, {"md5": md5})
            else:
                item = "数据重复，已过滤."
        else:
            self.db.insert(spider.name.replace("-", '_'), items)
        if "企业名称" in items.keys():
            company_name = items["企业名称"]
            company_name_md5 = ezfuc.md5(company_name)
            ret = self.db1.get("select md5 from company_md5 where md5='%s'" % company_name_md5)
            if not ret:
                self.db1.insert("company_name", {"企业名称": company_name})
                self.db1.insert("company_md5", {"md5": company_name_md5})
        self.count += 1
        return item

    def close_spider(self, spider):
        self.db.close()
        self.db1.close()
        if hasattr(spider, "filter_data") and spider.filter_data:
            spider.filter_conn.close()


class CreditPipeline(object):

    def __init__(self):
        self.host = config.sql_host
        self.username = config.sql_user
        self.password = config.sql_pwd
        self.database = 'zlcollector_credit'
        self.port = 3306
        self.db = MySql(self.host, self.database, self.username, self.password, self.port)
        self.db1 = MySql(self.host, "company", self.username, self.password, self.port)
        self.count = 0

    def open_spider(self, spider):
        if hasattr(spider, "filter_data") and spider.filter_data:
            if not hasattr(spider, "filter_db"):
                setattr(spider, "filter_db", "duplicate_key")
            if not hasattr(spider, "filter_table"):
                setattr(spider, "filter_table", "credit_%s" % spider.name.replace("-", "_"))
            spider.filter_conn = MySql(self.host, spider.filter_db, self.username, self.password, self.port)

    def process_item(self, item, spider):
        items = dict(item)
        if hasattr(spider, "filter_data") and spider.filter_data:
            md5 = items['md5']
            items.pop('md5')
            rest = spider.filter_conn.get("select md5 from %s where md5='%s'" % (spider.filter_table, md5))
            if not rest:
                self.db.insert(spider.name.replace("-", '_'), items)
                spider.filter_conn.insert(spider.filter_table, {"md5": md5})
                self.count += 1
            else:
                items = "数据重复，已过滤."
        else:
            self.db.insert(spider.name.replace("-", '_'), items)
            self.count += 1
        return items

    def close_spider(self, spider):
        if spider.way != 'm':
            if hasattr(spider, "total_count"):
                names = ('update_time', 'total_count', 'crawl_count')
                values = (str(datetime.datetime.now()), spider.total_count, self.count)
                spider.spider_db.update_spider_info(names, values, spider.queue_name)
            else:
                names = ('update_time', 'crawl_count')
                values = (str(datetime.datetime.now()), self.count)
                spider.spider_db.update_spider_info(names, values, spider.queue_name)
        self.db.close()
        self.db1.close()
        if hasattr(spider, "filter_data") and spider.filter_data:
            spider.filter_conn.close()