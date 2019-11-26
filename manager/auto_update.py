# -*- coding: utf-8 -*-
from sub.db import Database
from manager.run import auto_run
import config

from multiprocessing import Process
import datetime
import time


class AutoUpdate:
    def __init__(self):
        self.pool = []
        self.db = None
        self.table = None

    def gen_data(self):
        count = self.db.select_sql(self.table, select='count(*)', where="update_time is not null")
        count = count['count(*)']
        for i in range(0, count + 1, config.auto_step):
            ret = self.db.select_sql(self.table,
                                     where="update_time is not null and update_machine is not null and auto_frequency != -1",
                                     term=f"order by auto_frequency asc , update_time asc limit {i}, {config.auto_step}"
                                     )
            yield ret

    def run(self):
        for i in self.gen_data():
            print(i)
            if not i:
                continue
            if isinstance(i, list):
                cur = i[0]  # 最接近更新时间的那个脚本
            else:
                cur = i
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
                if diff_value < 0:
                    break
                print("最近一次更新时间在：%.3f小时后，稍等片刻···" % (diff_value / 60 / 60))
                time.sleep(diff_value)
                break
            print("***")
            p = Process(target=auto_run, args=(path, queue_name, 'auto', async_num))
            self.pool.append(p)
            p.start()
        for p in self.pool:
            if p.is_alive():
                p.join()

    def __enter__(self):
        print('begin!')
        self.db = Database(None)
        self.table = config.spider_db + '.' + config.spider_table

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.pool)
        for p in self.pool:
            if p.is_alive():
                print('kill process %s' % p.pid())
                p.terminate()  # 关闭孤儿进程


if __name__ == '__main__':
    a = AutoUpdate()
    with a:
        while True:
            a.run()
            time.sleep(1)
