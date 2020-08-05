# -*- coding: utf-8 -*-
from importlib import import_module
import datetime
import logging
import sys
sys.path.append(r"C:\Users\Dell\Desktop\spider_code")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

config = {

    'path': 'spider/BeiAn/B__48.py',
    'way': 'w',
    'async_num': 1,

}


def auto_run(path, queue_name, way, async_num):
    """自动跟新启动方法"""
    logging.info("爬虫启动时间：", datetime.datetime.now())
    spider_module = import_module(path.replace('/', '.').rstrip('.py'))
    sp = spider_module.Spider(path, queue_name, way, async_num)
    sp.main()
    logging.info("爬虫结束时间：", datetime.datetime.now())


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
            async_num = int(cmd[2])
            if '.py' in path:
                queue_name = '_'.join(path.rstrip('.py').split('/')[1:])
            else:
                queue_name = path
            print(path.replace('/', '.').rstrip('.py'))
            spider_module = import_module(path.replace('/', '.').rstrip('.py'))
        except Exception:
            logging.info("命令行格式错误")
            raise
    logging.info("爬虫启动时间：%s" % datetime.datetime.now())
    sp = spider_module.Spider(path, queue_name, way, async_num)
    pipeline = import_module("pipelines")
    pipelineObj = getattr(pipeline, "%sPipeline" % queue_name.split('_')[0])()
    pipelineObj.open_spider(sp)
    setattr(sp, "pipelineObj", pipelineObj)
    sp.main()
    pipelineObj.close_spider(sp)
    logging.info("爬虫结束时间：%s" % datetime.datetime.now())


if __name__ == '__main__':
    from sys import argv
    run(argv[1:])
