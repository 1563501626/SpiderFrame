# -*- coding: utf-8 -*-
import re

import fuclib
import scrapy
from pika import exceptions
import json as js
import asyncio
import threading
import functools
import traceback
import os
import time
import datetime
import socket
import logging
from collections import Generator
from scrapy.utils.reqser import request_to_dict

import config
import settings
from sub.queues import RabbitMq
from sub.db import Database
from sub.spiders import Request

logger = logging.getLogger(__name__)
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class DaemonRun(threading.Thread):
    def __init__(self, func, loop, *args, **kwargs):
        super(DaemonRun, self).__init__(*args, **kwargs)
        self.connector, self.channel = RabbitMq.mq_connection_from_config()
        self.func = func
        self.loop = loop
        self.setDaemon(True)

    def run(self) -> None:
        self.func(self.loop)


class Engine:
    """引擎"""

    purge = True
    allow_status_code = []
    max_times = 3
    domain = []
    timeout = 180
    proxy = False
    auto_frequency = -1  # 默认不自动更新
    cookie_update = False  # 默认不自动更新cookie
    start_urls = []
    custom_settings = {}
    priority_queue = False

    def __init__(self, path, queue_name, way, async_num):
        self.mq_host = None
        self.mq_port = None
        self.mq_user = None
        self.mq_pwd = None
        self.sql_host = None
        self.sql_port = None
        self.sql_user = None
        self.sql_pwd = None
        self.sql_db = None
        self.path = path
        self.async_num = async_num
        self.way = way
        self.queue_name = queue_name

        self.rabbit = None
        self.connector = None
        self.channel = None
        self.if_unused = False
        self.if_empty = False
        self.spider_db = None
        self.pool = None
        self.init_insql_lock = True
        self._settings = settings.__dict__

        self.loop = None
        self.request = None
        self.session = None
        self.update_machine = None
        self.count = 0
        self.thread = None

    def mq_connection(self):
        """rabbitmq连接"""
        self.rabbit = RabbitMq(self)
        return self.rabbit.mq_connection()

    def sql_connection(self):
        """数据库连接"""
        self.spider_db = Database(self)
        return self.spider_db.db_pool()

    def produce(self, url=None, params=None, data=None, json=None, charset=None, cookies=None, method='get', headers=None,
                callback="parse", proxies=None, allow_redirects=True, meta={}, time_out=None, not_request=None, priority=1):
        """生产"""
        if not isinstance(callback, str):
            callback = callback.__name__
        if not_request or (isinstance(url, str) and not re.search(r"^https?://", url)):
            request = {'not_request': True,
                       'url': url,
                       'callback': callback,
                       'meta': meta
                       }
        else:
            if isinstance(url, dict):
                ret = url
                request = {
                    'url': ret['url'],
                    'params': ret.get('params'),
                    'data': ret.get('data', ret.get('body')),
                    'json': ret.get('json'),
                    'charset': ret.get('charset'),
                    'cookies': ret.get('cookies'),
                    'method': ret.get('method', 'GET'),
                    'headers': ret.get('headers'),
                    'callback': ret.get('callback') if ret.get('callback') else 'parse',
                    'allow_redirects': ret.get('allow_redirects') if ret.get('allow_redirects') else True,
                    'meta': ret.get('meta') if ret.get('meta') else {},
                    'url_encoded': True if '%' in ret['url'] else False,
                    'priority': ret.get('priority', 1)
                }
            else:
                request = {
                    'url': url,
                    'params': params,
                    'data': data,
                    'json': json,
                    'charset': charset,
                    'cookies': cookies,
                    'method': method,
                    'headers': headers,
                    'callback': callback,
                    'allow_redirects': allow_redirects,
                    'meta': meta,
                    'url_encoded':  True if '%' in url else False,
                    'priority': priority
                }
        if request['data']:
            request['method'] = 'post'
        if self.thread:
            self.rabbit.publish(self.thread.channel, js.dumps(request), self.queue_name, priority=request['priority'])
        else:
            self.rabbit.publish(self.channel, js.dumps(request), self.queue_name, priority=request['priority'])
        self.count += 1
        logger.info("(%s) %s生产：%s" % (self.name, self.count, js.dumps(request)))

    def consume(self):
        """消费"""
        while True:
            try:
                self.connector, self.channel = self.rabbit.sure_conn(self.queue_name, self.connector, self.channel)
                self.rabbit.consume(self.channel, self.queue_name, callback=self.callback, prefetch_count=self.async_num)
                break
            except exceptions.ConnectionClosed:
                self.connector, self.channel = self.rabbit.mq_connection()
                print('-', "pika.exceptions.ConnectionClosed", time.ctime())

    @staticmethod
    def run_forever(loop):
        """实时接收新事件"""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def start_requests(self):
        """抽象生产函数"""
        if self.start_urls:
            for url in self.start_urls:
                self.produce(url)

    def parse(self, response):
        """抽象解析函数"""
        pass

    def before_request(self, ret):
        """请求中间件"""
        return ret

    async def deal_resp(self, ch, method, properties, ret):
        """请求并回调处理响应函数"""
        try:
            response = await self.request.quest(self.session, ret, self.max_times)
            if response and (response.status_code in self.allow_status_code or response.status_code == 200):
                try:
                    self.routing(self.__getattribute__(ret['callback']), response)
                except Exception as e:
                    self.connector.add_callback_threadsafe(functools.partial(ch.basic_nack, method.delivery_tag))
                    traceback.print_exc()
                    self.deal_error(e)
                self.connector.add_callback_threadsafe(functools.partial(ch.basic_ack, method.delivery_tag))
            elif response:
                logger.info("(%s) 请求失败!返回状态码：%d,返回队列%s" % (self.name, response.status_code, ret))
                self.produce(ret)
                self.connector.add_callback_threadsafe(functools.partial(ch.basic_ack, method.delivery_tag))
            else:
                logger.info("(%s) 请求报错!未返回消息,返回队列%s" % (self.name, ret))
                self.produce(ret)
                self.connector.add_callback_threadsafe(functools.partial(ch.basic_ack, method.delivery_tag))
        except Exception as e:
            traceback.print_exc()
            self.deal_error(e)

    def deal_error(self, e):
        if self.way == 'auto':
            names = ("error_type", "auto_frequency")
            values = (e.args[0], -1)
            db = Database(None)
            db.update_spider_info(names, values, self.queue_name)
            logger.info("自动更新报错。")
        os._exit(1)

    def spider_info_init(self):
        """爬虫信息初始化入库"""
        ret = self.spider_db.select_sql(table=config.spider_db + '.' + config.spider_table,
                                        where=f'queue_name="{self.queue_name}"', one=True)
        if not ret:
            # 首次入库
            logger.info("初始化.")
            now_time = str(datetime.datetime.now())
            names = ('path', 'queue_name', 'auto_frequency', 'cookie_update', 'create_time', 'update_machine')
            values = (self.path, self.queue_name, -1, self.cookie_update, now_time, self.update_machine)
            self.spider_db.in_sql(config.spider_db + '.' + config.spider_table, names, values)
        else:
            # 是否存在重要配置更新
            auto_frequency = ret['auto_frequency']
            update_machine = ret['update_machine']
            if auto_frequency != self.auto_frequency:
                if self.update_machine not in update_machine.split(','):
                    names = ('auto_frequency', 'update_machine')
                    values = (self.auto_frequency, self.update_machine)
                else:
                    names = ('auto_frequency',)
                    values = (self.auto_frequency,)
                self.spider_db.update_spider_info(names, values, self.queue_name)
            self.cookie_update = ret['cookie_update']

    def pipeline(self, item):
        pipelineObj = getattr(self, "pipelineObj")
        ret = pipelineObj.process_item(item, self)
        logger.info("(%s) %s：%s" % (self.name, pipelineObj.count, ret))  # todo

    async def deal(self, ch, method, properties, ret):
        try:
            self.routing(self.__getattribute__(ret['callback']), ret)
            self.connector.add_callback_threadsafe(functools.partial(ch.basic_ack, method.delivery_tag))
        except Exception as e:
            traceback.print_exc()
            self.deal_error(e)

    def callback(self, ch, method, properties, body):
        """rabbit_mq回调函数"""
        if body:
            result = body.decode()
        else:
            raise
        ret = js.loads(result)
        ret = self.before_request(ret)
        if 'not_request' in ret:
            logger.info('(%s)消费：%s' % (self.name, ret))
            coroutine = self.deal(ch, method, properties, ret)
            asyncio.run_coroutine_threadsafe(coroutine, self.loop)
        else:
            ret['time_out'] = self.timeout
            if not ret['headers']:
                ret['headers'] = {"User-Agent": fuclib.ezfuc.random_ua()}  # todo
            if self.proxy:
                proxy_res = fuclib.getIP()
                if proxy_res:
                    ret['proxies'] = proxy_res['proxy']
                    # ret['headers']["Proxy-Authorization"] = fuclib.proxyAuth
            logger.info('(%s)消费：%s' % (self.name, ret))

            coroutine = self.deal_resp(ch, method, properties, ret)
            asyncio.run_coroutine_threadsafe(coroutine, self.loop)

    def decode_request(self, request: dict):
        """从scrapy传过来的Request对象部分键值为byte类型"""
        result = {}
        for k, v in request.items():
            if isinstance(k, bytes):
                new_k = k.decode()
            else:
                new_k = k
            if isinstance(v, bytes):
                new_v = v.decode()
            elif isinstance(v, dict):
                new_v = self.decode_request(v)
            elif isinstance(v, (list, tuple)):
                if len(v) > 1:
                    raise
                if not v:
                    new_v = ''
                else:
                    new_v = v[0].decode() if isinstance(v[0], bytes) else v[0]
            else:
                new_v = v
            result[new_k] = new_v
        return result

    def routing(self, function, *args, **kwargs):
        result_type = function(*args, **kwargs)
        if isinstance(result_type, Generator):
            for i in result_type:
                if isinstance(i, scrapy.Request):  # 通过yield过来的请求
                    request = self.decode_request(request_to_dict(i, self))
                    self.produce(request)
                elif isinstance(i, scrapy.Item):
                    self.pipeline(i)
                else:
                    raise
        elif isinstance(result_type, scrapy.Request):
            request = self.decode_request(request_to_dict(result_type, self))  # 通过return过来的请求
            self.produce(request)
        elif isinstance(result_type, scrapy.Item):
            self.pipeline(result_type)

    def main(self):
        """启动函数"""
        # 配置文件初始化
        serious = ['mq_host', 'mq_port', 'mq_user', 'mq_pwd', 'sql_host', 'sql_port', 'sql_user', 'sql_pwd', 'sql_db']
        for i in serious:
            if hasattr(self, i) and getattr(self, i) is None:
                attr = getattr(config, i)
                setattr(self, i, attr if attr else None)
        self._settings.update(self.custom_settings)
        self._settings.setdefault('DOWNLOADER_MIDDLEWARES', {'DOWNLOADER_MIDDLEWARES':
                                                                 {'frame.tools.middleware.DownloaderMiddleware': 1}})
        if 'ProxyMiddleware' in self._settings['DOWNLOADER_MIDDLEWARES']:
            self.proxy = True

        # 创建连接
        self.connector, self.channel = self.mq_connection()
        self.pool = self.sql_connection()
        logger.info('rabbitmq配置：%s' % [self.mq_host, self.mq_port, self.mq_user])
        logger.info('sql配置：%s' % [self.sql_host, self.sql_port, self.sql_user, self.sql_db])

        # 脚本信息入库
        self.update_machine = socket.gethostbyname(socket.gethostname())
        logger.info("本机ip为：%s" % self.update_machine)
        self.spider_info_init()

        # 生产消费
        if self.way and (self.way == 'm' or self.way == 'auto'):
            if self.priority_queue:
                self.channel.queue_declare(queue=self.queue_name, durable=True, arguments={"x-max-priority": 10})
            else:
                self.channel.queue_declare(queue=self.queue_name, durable=True)
            if self.purge:
                RabbitMq.purge(self.channel, self.queue_name)
            else:
                logger.info("继续生产!!!")
            self.routing(self.start_requests)
        if self.way and (self.way == 'w' or self.way == 'auto'):
            self.request = Request()
            self.loop = asyncio.new_event_loop()
            self.session = self.loop.run_until_complete(self.request.new_session())

            self.thread = DaemonRun(self.run_forever, self.loop)
            self.thread.start()

            self.consume()

            asyncio.run_coroutine_threadsafe(self.request.exit(self.session), self.loop)
        if not self.way or self.way not in ('m', 'w', 'auto'):
            raise

        # 退出并释放资源
        self.channel.close()
        self.pool.close()


Spider = Engine
