# -*- coding: utf-8 -*-
from sub.db import Database
from manager.run import auto_run
import config

from multiprocessing import Process
import datetime
import time


db = Database(None)
conn = db.db_pool(sql_host=config.spider_host, sql_user=config.spider_user, sql_pwd=config.spider_pwd,
                  sql_db=config.spider_db, sql_port=config.spider_port)


def gen_data():
    cursor = conn.cursor()
    count = db.select_sql(config.spider_table, select='count(*)', where="update_time is not null", cursor=cursor)
    count = count['count(*)']
    for i in range(0, count+1, config.auto_step):
        ret = db.select_sql(config.spider_table,
                            where="update_time is not null and update_machine is not null and auto_frequency != -1",
                            term=f"order by auto_frequency asc , update_time asc limit {i}, {config.auto_step}",
                            cursor=cursor)
        yield ret


def deal_err(err):
    print(err)


def main():
    ps = []
    for i in gen_data():
        print(i)
        cur = i[0]  # 最接近更新时间的那个脚本
        path = cur['path']
        auto_frequency = cur['auto_frequency'] * 60 * 60  # hour -> seconds
        update_time = cur['update_time']
        queue_name = cur['queue_name']
        async_num = cur['async_num']
        now_time = datetime.datetime.now()
        diff_value = (now_time - update_time).seconds
        while diff_value < auto_frequency:
            now_time = datetime.datetime.now()
            diff_value = (now_time - update_time).seconds
            print("最近一次更新时间在：%.3f小时后，稍等片刻···" % (diff_value / 60 / 60))
            time.sleep(diff_value)
        p = Process(target=auto_run, args=(path, queue_name, 'auto', async_num))
        ps.append(p)
        p.start()
    for p in ps:
        if p.is_alive():
            p.join()


if __name__ == '__main__':
    main()
