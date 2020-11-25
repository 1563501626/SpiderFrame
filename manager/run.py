# -*- coding: utf-8 -*-
import settings
from importlib import import_module
import datetime
import logging
import settings
from tools.loadspider import SpiderLoader

logging.basicConfig(level=getattr(logging, getattr(settings, 'LOG_LEVEL', 'INFO')),
                    format='pid:%(process)d %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    # filename='debug.txt',
                    # filemode='a'
                    )

config = {
    'path': 'Apt',
    'name': 'SK--2',
    'way': 'w',
    'async_num': 1,
}


def auto_run(root_path, spider_name, way, async_num):
    """自动跟新启动方法"""
    logging.info("爬虫启动")
    base_path = settings.SPIDER_MODULE + '.'
    path = base_path + root_path
    queue_name = root_path + '/' + spider_name
    sl = SpiderLoader(type("settings", (object,), dict(getlist=lambda x: [path], getbool=lambda x: False)))
    spider_module = sl.load(spider_name)
    sp = spider_module(path=path, queue_name=queue_name, way=way, async_num=async_num)
    pipeline = import_module("pipelines")
    pipelineObj = getattr(pipeline, "%sPipeline" % root_path, getattr(pipeline, 'Pipeline'))()
    pipelineObj.open_spider(sp)
    setattr(sp, "pipelineObj", pipelineObj)
    sp.main()
    pipelineObj.close_spider(sp)
    logging.info("爬虫结束")


def run(cmd: list = None) -> None:
    """手动启动方法"""
    base_path = settings.SPIDER_MODULE + '.'
    if not cmd:
        path = base_path + config['path']
        root_path = config['path']
        spider_name = config['name']
        queue_name = config['path']+'/'+spider_name
        way = config['way']
        async_num = config['async_num']
    else:
        try:
            path = base_path + cmd[0]
            root_path = cmd[0]
            spider_name = cmd[1]
            way = cmd[2]
            async_num = int(cmd[3])
            queue_name = cmd[0]+'/'+spider_name
        except Exception:
            logging.info("命令行格式错误")
            raise
    logging.info("爬虫启动时间：%s" % datetime.datetime.now())
    sl = SpiderLoader(type("settings", (object,), dict(getlist=lambda x: [path], getbool=lambda x: False)))
    spider_module = sl.load(spider_name)
    sp = spider_module(path=path, queue_name=queue_name, way=way, async_num=async_num)
    pipeline = import_module("pipelines")
    pipelineObj = getattr(pipeline, "%sPipeline" % root_path, getattr(pipeline, 'Pipeline'))()
    pipelineObj.open_spider(sp)
    setattr(sp, "pipelineObj", pipelineObj)
    sp.main()
    pipelineObj.close_spider(sp)
    logging.info("爬虫结束时间：%s" % datetime.datetime.now())


if __name__ == '__main__':
    from sys import argv
    run(argv[1:])
