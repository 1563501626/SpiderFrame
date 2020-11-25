# -*- coding: utf-8 -*-
import sys, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from tools.loadspider import SpiderLoader
from sub.db import Database
from manager.run import auto_run
import config

from multiprocessing import Process, Pool

import datetime
import time
import logging

logger = logging.getLogger(__name__)


class AutoUpdate:
    def __init__(self):
        self.pool = []
        self.db = None
        self.table = None

    def gen_data(self):
        count = self.db.select_sql(self.table, select='count(*)', where="update_time is not null")
        count = count['count(*)']
        for i in range(0, count + 1, config.auto_step):
            ret = self.db.select_sql(
                self.table,
                where="update_time is not null and update_machine is not null and auto_frequency != -1",
                term=f"order by auto_frequency asc , update_time asc limit {i}, {config.auto_step}"
            )
            yield ret

    def run(self):
        for i in self.gen_data():
            logger.info("*****************************************************************************************")
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
                logger.info("最近一次更新时间在：%.3f小时后，稍等片刻···" % (diff_value / 60 / 60))
                time.sleep(diff_value)
                break
            p = Process(target=auto_run, args=(path, queue_name, 'auto', async_num))
            self.pool.append(p)
            p.start()
        for p in self.pool:
            p.join()
            if p.is_alive():
                logger.info('kill process %s' % p.pid())
                p.terminate()
            else:
                self.pool.remove(p)
            logger.info(self.pool)

    def __enter__(self):
        logger.info('begin!')
        self.db = Database(None)
        self.table = config.spider_db + '.' + config.spider_table
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('exit!')
        for p in self.pool:
            if p.is_alive():
                logger.info('kill process %s' % p.pid())
                p.terminate()  # 关闭孤儿进程


class OperateUpdate:
    def __init__(self, update_li, abs_path):
        self.update_li = update_li
        self.abs_path = abs_path
        # self.pool = Pool(len(update_li))
        self.pids = {}

    def run(self):
        for spider_name in self.update_li:
            path = self.abs_path
            async_num = 1
            p = Process(target=auto_run, args=(path, spider_name, 'auto', async_num))
            p.start()
            self.pids[spider_name] = p.pid
        with open(r"pidSpiderMap.txt", 'a') as f:
            f.write(datetime.datetime.now().strftime("%F") + str(self.pids) + '\n')


def beian(which):
    path = "example"
    if which == '1':  # 周一 'B--3','B--37','B--38',
        names = ['B--31', 'B--13', 'B--55', 'B--117', 'B--42', 'B--67', 'B--8', 'B--5', 'B--116', 'B--36',
                 'B--23', 'B--97', 'B--33', 'B--34', 'B--16', 'B--118', 'B--119', 'B--120', 'B--121',
                 'B--122', ]

    elif which == '2':  # 'B--106','B--111',
        names = ['B--21', 'B--27', 'B--123', 'B--124', 'B--125', 'B--10', 'B--105', 'B--126', 'B--115',
                 'B--44', 'B--107', 'B--28', 'B--49', 'B--50', 'B--51', 'B--102', 'B--52', 'B--53', 'B--26',
                 'B--114', 'B--59', 'B--60', 'B--108', 'B--127']

    elif which == '3':
        names = ['B--63', 'B--101', 'gansu']

    elif which == '6':
        names = ['B--19', 'B--48', 'B--45', 'B--25', 'B--113']

    op = OperateUpdate(names, path)
    op.run()


def apt(types):
    ignore = ["k--115","K--170", "K--187", "k--189", "k--199", "k--59","k--92","k--93","k112"]  # 暂停采集
    path = "Apt"
    if types == '施工设计':
        # "k--15",  "k--24"手动跑  ,暂停采集

        names = ["k--135",  "K--171", "k--151", "k--103", "k--142",
                 "k--43", "k--16-2", "k--99", "k--145",  "K--175",
                 "k--126", "k--172", "k--188",   "k94",
                 "k--123", "k--182", "k--107", "k--110", "k83", "k4", "k--20", "K--194", "k--23", ]
    elif types == '压力管道':
        names = ['SK--2', 'SK--3', 'SK--4', 'SK--5', 'SK--6', 'SK--7', 'SK--10', 'SK--11', 'SK--13', 'SK--14', 'SK--15',
                 'SK--16', 'SK--18', 'SK--20', 'SK--21', 'SK--25', 'SK--26', 'SK--27', 'SK--28', 'SK--29', 'SK--32',
                 'SK--33',
                 'SK--34', 'SK--35', 'SK--36', 'SK--37', 'SK--38', 'SK--39', 'SK--41']
    elif types == '小资质':
        today = datetime.datetime.now().isoweekday()
        if today == 1:
            table_li = ['1--201', '1--202', '1--203']  # 周一
        elif today == 2:  #
            table_li = ['GK--24', 'GK--4', 'K--4_', 'K--5', 'k--1']  # 周二
        elif today == 3:
            table_li = ['K--7', 'K--9', 'K--11', 'K--20_', ]  # 周三
        elif today == 4:
            table_li = ['K--12', 'GK--9', 'GK--10', 'SK--42', "K--40"]  # 周四
        elif today == 5:
            table_li = ['K--19', 'K--25', 'K--37']  # 周五
        names = table_li
    op = OperateUpdate(names, path)
    op.run()


def credit(t=0):
    today = datetime.datetime.now().isoweekday()
    path = "Credit"
    if t == 9:
        table_li = ["X--11", "X--12", "X--13", ]
    else:
        table_li = ["X--8", "X--9", "X--35", "X--36", "X--37", "X--64", "X--65", "X--73", "X--74", "X--25",
                    "X--85", "X--88", "X--89", "X--90", "X--91", "X--44", "X--60", "X--61", "X--62", "X--63", "X--96"]
    if today == 1:
        table_li += ['X--19', "X--20", "X--41", "X--42"]  # 周一
    elif today == 2:
        table_li += ['X--24', "X--29"]  # 周二
    elif today == 3:
        if t == 9:
            table_li += ["X--10", "X--14", "X--15", "X--16", "X--17", "X--18"]  # 周三
        else:
            table_li += ['x--5', "x--21", ]  # 周三

    # table_li = ['X--70', "X--71", 'X--72', 'X--75', 'X--78', 'X--79', 'X--80',]  # 每月1号
    names = table_li
    op = OperateUpdate(names, path)
    op.run()


def urplan():
    path = 'URPlan'
    module = 'spider_code.spider.URPlan'
    sl = SpiderLoader(type("settings", (object,), dict(getlist=lambda x: [module], getbool=lambda x: False)))
    names = sl.list()
    op = OperateUpdate(names, path)
    op.run()


def cost():
    path = 'cost'
    module = 'spider_code.spider.cost'
    sl = SpiderLoader(type("settings", (object,), dict(getlist=lambda x: [module], getbool=lambda x: False)))
    names = sl.list()
    op = OperateUpdate(names, path)
    op.run()


def routing(kind):
    if kind == '施工设计':  # 周一，周三
        apt(kind)
    elif kind == '压力管道':
        apt(kind)
    elif kind == '小资质':
        apt(kind)
    elif kind == '信用评价':
        credit()
    elif kind == '信用评价9':  # 9点后跑
        credit(9)
    elif kind == '造价咨询':  # 每周四
        cost()
    else:
        print("函数未定义.")
        time.sleep(10)


if __name__ == '__main__':
    # with AutoUpdate() as a:
    #     while True:
    #         a.run()
    #         time.sleep(1)
    # beian('2')
    # apt("施工设计")  # 周一，周三
    # apt("压力管道")
    # apt("小资质")

    credit()
    # urplan()
    # test()
    # credit(9)  # 9点后跑
    # cost()  # 每周四

    print()
