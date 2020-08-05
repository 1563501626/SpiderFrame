# -*- coding: utf-8 -*-
import fuclib
from pika import exceptions
import config
from sub.pipeline import RabbitMq
from sub.db import Database
from sub.spiders import Request

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

logger = logging.getLogger(__name__)


class Heartbeat(threading.Thread):
    """心跳线程类"""

    def __init__(self, connector):
        super(Heartbeat, self).__init__()
        self.lock = threading.Lock()
        self.connection = connector
        self.quit_flag = False  # 退出标志
        self.stop_flag = True  # 暂停标志
        self.setDaemon(True)
        # self.queue_name = queue_name
        # self.channel = channel
        # self.spider_db = self.engine.spider_db
        self.flag = 0

    def run(self):
        while not self.quit_flag:
            time.sleep(10)
            self.flag += 10
            # if self.flag % config.get_queue_info_delay == 0:
            #     # 负责监听队列，当队列Total==0时，更新自动更新时间并删除队列退出程序
            #     r = RabbitMq.is_empty(self.queue_name)
            #     if not r:
            #         names = ('update_time', 'auto_frequency')
            #         values = (str(datetime.datetime.now()), self.engine.auto_frequency)
            #         self.spider_db.update_spider_info(names, values, self.queue_name)
            #         RabbitMq.del_queue(self.channel, self.queue_name)
            self.lock.acquire()
            if self.stop_flag:
                self.lock.release()
                continue
            try:
                self.connection.add_callback_threadsafe(self.connection.process_data_events)  # 一直等待服务段发来的消息
            except Exception as e:
                logger.info("rabbitmq连接丢失: %s" % (str(e)))
                self.lock.release()
                return
            self.lock.release()

    def start_heartbeat(self):
        self.lock.acquire()
        if self.quit_flag:
            self.lock.release()
            return
        self.stop_flag = False
        self.lock.release()


class DaemonRun(threading.Thread):
    def __init__(self, func, loop, *args, **kwargs):
        super(DaemonRun, self).__init__(*args, **kwargs)
        self.connector, self.channel = RabbitMq.mq_connection_from_config()
        self.func = func
        self.loop = loop
        self.setDaemon = True

    def run(self) -> None:
        self.func(self.loop)


class Engine:
    """引擎"""

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

        self.purge = True
        self.loop = None
        self.request = None
        self.session = None
        self.allow_status_code = []
        self.max_times = 3

        self.domain = []
        self.update_machine = None
        self.timeout = None
        self.proxy = False
        self.auto_frequency = -1  # 默认不自动更新
        self.cookie_update = False  # 默认不自动更新cookie

        self.start_urls = []
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

    def produce(self, url, params=None, data=None, json=None, charset=None, cookies=None, method='get', headers=None,
                callback="parse", proxies=None, allow_redirects=True, meta=None):
        """生产"""
        if not isinstance(callback, str):
            callback = callback.__name__
        if isinstance(url, dict):
            ret = url
            request = {
                'url': ret['url'],
                'params': ret['params'],
                'data': ret['data'],
                'json': ret['json'],
                'charset': ret['charset'],
                'cookies': ret['cookies'],
                'method': ret['method'],
                'headers': ret['headers'],
                'callback': ret['callback'],
                'proxies': ret['proxies'],
                'allow_redirects': ret['allow_redirects'],
                'meta': ret['meta']
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
                'proxies': proxies,
                'allow_redirects': allow_redirects,
                'meta': meta
            }
        if self.thread:
            self.rabbit.publish(self.thread.channel, js.dumps(request), self.queue_name)
        else:
            self.rabbit.publish(self.channel, js.dumps(request), self.queue_name)
        self.count += 1
        logger.info("%s 生产：%s" % (self.count, js.dumps(request)))

    def consume(self):
        """消费"""
        # h = Heartbeat(self.connector)
        # h.start()
        # h.start_heartbeat()
        # self.connector.process_data_events()
        while True:
            print('***')
            try:
                self.connector, self.channel = self.rabbit.sure_conn(self.queue_name, self.connector, self.channel)
                self.rabbit.consume(self.channel, self.queue_name, callback=self.callback, prefetch_count=self.async_num)
                break
            except exceptions.ConnectionClosed:
                self.connector, self.channel = self.rabbit.mq_connection()
                print('-', "pika.exceptions.ConnectionClosed", time.ctime())
        # self.rabbit.consume(self.channel, self.queue_name, callback=self.callback, prefetch_count=self.async_num)

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
                self.__getattribute__(ret['callback'])(response)
                self.connector.add_callback_threadsafe(functools.partial(ch.basic_ack, method.delivery_tag))
            elif response:
                logger.info("请求失败!返回状态码：%d,返回队列%s" % (response.status_code, ret))
                # self.produce(ret)
                self.connector.add_callback_threadsafe(functools.partial(ch.basic_nack, method.delivery_tag))
            else:
                logger.info("请求报错!未返回消息,返回队列%s" % ret)
                # self.produce(ret)
                self.connector.add_callback_threadsafe(functools.partial(ch.basic_nack, method.delivery_tag))
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
        logger.info("%s：%s" % (pipelineObj.count, ret))

    def callback(self, ch, method, properties, body):
        """rabbit_mq回调函数"""
        if body:
            result = body.decode()
        else:
            raise
        ret = js.loads(result)
        ret = self.before_request(ret)
        ret['time_out'] = self.timeout
        if not ret['headers']:
            ret['headers'] = {"User-Agent": fuclib.ezfuc.random_ua()}
        if self.proxy:
            proxy_res = fuclib.getIP()
            if proxy_res:
                ret['proxies'] = proxy_res['proxy']
                ret['headers']["Proxy-Authorization"] = fuclib.proxyAuth
        logger.info('消费：%s' % ret)

        coroutine = self.deal_resp(ch, method, properties, ret)
        asyncio.run_coroutine_threadsafe(coroutine, self.loop)

    def main(self):
        """启动函数"""
        # 配置文件初始化
        serious = ['mq_host', 'mq_port', 'mq_user', 'mq_pwd', 'sql_host', 'sql_port', 'sql_user', 'sql_pwd', 'sql_db']
        for i in serious:
            if hasattr(self, i) and getattr(self, i) is None:
                attr = getattr(config, i)
                setattr(self, i, attr if attr else None)

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
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            if self.purge:
                RabbitMq.purge(self.channel, self.queue_name)
            else:
                logger.info("继续生产!!!")
            self.start_requests()
        if self.way and (self.way == 'w' or self.way == 'auto'):
            self.request = Request()
            self.loop = asyncio.new_event_loop()
            self.session = self.loop.run_until_complete(self.request.new_session())

            # thread = threading.Thread(target=self.run_forever, args=(self.loop,))
            # thread.setDaemon(True)
            # thread.start()

            self.thread = DaemonRun(self.run_forever, self.loop)
            self.thread.start()

            self.consume()

            asyncio.run_coroutine_threadsafe(self.request.exit(self.session), self.loop)
        if not self.way or self.way not in ('m', 'w', 'auto'):
            raise

        # 退出并释放资源
        self.channel.close()
        self.pool.close()
