# -*- coding: utf-8 -*-
from spider_code.confs import getConfig
from fuclib import ezfuc
conf = getConfig.get_config()

ezfuc.init()
file_object = open(r'W:\ZLCollector\ZLCollector_Beian\spider_code\libs\企业名后缀.txt', 'r', encoding="utf-8")
task_list=[ezfuc.replace_plus(i, ['\n','\ufeff']) for i in file_object]
file_object.close()


class manage_sql:
    @classmethod
    def save_myssql(cls,sql,*arge):
        if len(arge):
            with conf.pymssql.connect(host=conf.wlj_host, user=conf.wlj_user, password=conf.wlj_password, database=conf.wlj_database, charset="utf8") as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql,arge[0])
                    conn.commit()
        else:
            with conf.pymssql.connect(host=conf.wlj_host, user=conf.wlj_user, password=conf.wlj_password, database=conf.wlj_database, charset="utf8") as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    conn.commit()

    @classmethod
    def read_myssql(cls,sql):
        with conf.pymssql.connect(host=conf.wlj_host, user=conf.wlj_user, password=conf.wlj_password, database=conf.wlj_database, charset="utf8") as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()