# -*- coding: utf-8 -*-
from importlib import import_module
import datetime


config = {

    'path':'spider/test.py',
    'way':'w',
    'async_num':20,

}


def run():
    queue_name = config['path'].replace('/', '_').rstrip('.py')
    way = config['way']
    async_num = config['async_num']
    spider_moudel = import_module(queue_name.replace('_', '.'))
    print("爬虫启动时间：", datetime.datetime.now())
    sp = spider_moudel.Spider(queue_name, way, async_num)
    sp.main()
    print("爬虫结束时间：", datetime.datetime.now())

run()