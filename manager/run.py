# -*- coding: utf-8 -*-
from importlib import import_module
import datetime


config = {

    'path':'spider/test.py',
    'way':'w',
    'async_num':1,

}


def run():
    queue_name = '_'.join(config['path'].rstrip('.py').split('/')[1:])
    way = config['way']
    async_num = config['async_num']
    spider_moudel = import_module(config['path'].replace('/', '.').rstrip('.py'))
    print("爬虫启动时间：", datetime.datetime.now())
    sp = spider_moudel.Spider(queue_name, way, async_num)
    sp.main()
    print("爬虫结束时间：", datetime.datetime.now())


if __name__ == '__main__':
    run()
