# -*- coding: utf-8 -*-
from sub.db import Database
from manager.run import run
import config

import multiprocessing
import datetime
import time


def get_connection():
    """获取数据库连接"""
    db = Database(None)
    conn = db.db_pool(sql_host=config.spider_host, sql_user=config.spider_user, sql_pwd=config.spider_pwd,
                      sql_db=config.spider_db, sql_port=config.spider_port)
    return db, conn


def gen_data():
    db, conn = get_connection()
    cursor = conn.cursor()
    count = db.select_sql(config.spider_table, select='count(*)', where="update_time is not null", cursor=cursor)
    count = count['count(*)']
    for i in range(0, count+1, config.auto_step):
        ret = db.select_sql(config.spider_table, where="update_time is not null and update_machine is not null",
                            term=f"order by auto_frequency asc , update_time asc limit {i}, {config.auto_step}",
                            cursor=cursor)
        yield db, ret


def main():
    pool = multiprocessing.Pool()
    for db, i in gen_data():
        print(i)
        cur = i[0]  # 最接近更新时间的那个脚本
        auto_frequency = cur['auto_frequency'] * 60 * 60  # hour -> seconds
        update_time = cur['update_time']
        queue_name = cur['queue_name']
        async_num = cur['async_num']
        cookie_update = cur['cookie_update']
        now_time = datetime.datetime.now()
        diff_value = (now_time - update_time).seconds
        while diff_value < auto_frequency:
            now_time = datetime.datetime.now()
            diff_value = (now_time - update_time).seconds
            print(f"最近一次更新时间在：{diff_value / 60 / 60}小时后，稍等片刻···")
            time.sleep(diff_value)
        try:
            pool.apply_async(run, args=([queue_name, 'auto', async_num], cookie_update=cookie_update))
        except Exception as e:
            names = ("error_type", "auto_frequency")
            values = (e.args[0], -1)
            db.update_spider_info(names, values, queue_name)
            raise e
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
