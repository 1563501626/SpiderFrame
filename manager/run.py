# -*- coding: utf-8 -*-
from importlib import import_module
import datetime


config = {

    'path':'spider/hj/hh.py',
    'way':'w',
    'async_num':4,

}


def auto_run(path, queue_name, way, async_num):
    """自动跟新启动方法"""
    print("爬虫启动时间：", datetime.datetime.now())
    spider_module = import_module(path.replace('/', '.').rstrip('.py'))
    sp = spider_module.Spider(path, queue_name, way, async_num)
    sp.main()
    print("爬虫结束时间：", datetime.datetime.now())


def run(cmd: list = None):
    """手动启动方法"""
    if not cmd:
        path = config['path']
        queue_name = '_'.join(config['path'].rstrip('.py').split('/')[1:])
        way = config['way']
        async_num = config['async_num']
        spider_module = import_module(config['path'].replace('/', '.').rstrip('.py'))
    else:
        try:
            path = cmd[0]
            way = cmd[1]
            async_num = cmd[2]
            if '.py' in path:
                queue_name = '_'.join(path.rstrip('.py').split('/')[1:])
            else:
                queue_name = path
            spider_module = import_module(path.replace('/', '.').rstrip('.py'))
        except Exception:
            print("命令行格式错误")
            raise
    print("爬虫启动时间：", datetime.datetime.now())
    sp = spider_module.Spider(path, queue_name, way, async_num)
    sp.main()
    print("爬虫结束时间：", datetime.datetime.now())


if __name__ == '__main__':
    from sys import argv
    run(argv[1:])
