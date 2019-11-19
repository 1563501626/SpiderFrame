# -*- coding: utf-8 -*-
import config
from sub.scheduler import RabbitMq
from sub.item_pipline import Database
from sub.spiders import Request

import json as js
import asyncio
import threading
import functools
import traceback
import sys
import time


class Heartbeat(threading.Thread):
    """
    在同步消息消费的时候可能会出现pika库断开的情况，原因是因为pika客户端没有及时发送心跳，连接就被server端断开了。
    解决方案就是做一个心跳线程来维护连接。
    """
    def __init__(self, connection, channel, queue_name):
        super(Heartbeat, self).__init__()
        self.lock = threading.Lock()  # 线程锁
        self.connection = connection  # rabbit连接
        self.quitflag = False  # 退出标志
        self.stopflag = True  # 暂停标志
        self.setDaemon(True)  # 设置为守护线程，当消息处理完，自动清除
        self.queue_name = queue_name
        self.channel = channel
        self.flag = 0

    # 间隔10s发送心跳
    def run(self):
        while not self.quitflag:
            time.sleep(10)  # 睡10s发一次心跳
            self.flag += 10
            if self.flag % 60 == 0:
                if not RabbitMq.is_empty(self.queue_name):
                    RabbitMq.del_queue(self.channel, self.queue_name)
            self.lock.acquire()  # 加线程锁
            if self.stopflag:
                self.lock.release()
                continue
            try:
                self.connection.process_data_events()  # 一直等待服务段发来的消息
            except Exception as e:
                print("rabbitmq连接丢失: %s" % (str(e)))
                self.lock.release()
                return
            self.lock.release()

    # 开启心跳保护
    def startheartbeat(self):
        self.lock.acquire()
        if self.quitflag:
            self.lock.release()
            return
        self.stopflag = False
        self.lock.release()


class Engine:
    def __init__(self, queue_name, way, async_num=1):
        self.mq_host = None
        self.mq_port = None
        self.mq_user = None
        self.mq_pwd = None
        self.sql_host = None
        self.sql_port = None
        self.sql_user = None
        self.sql_pwd = None
        self.sql_db = None
        self.async_num = async_num
        self.way = way
        self.queue_name = queue_name
        self.timeout = None

        self.rabbit = None
        self.connector = None
        self.channel = None
        self.if_unused = False
        self.if_empty = False
        self.cursor = None

        self.purge = True
        self.loop = None
        self.request = None
        self.session = None
        self.allow_status_code = []
        self.retry = 3

    def mq_connection(self):
        """rabbitmq连接"""
        self.rabbit = RabbitMq(self)
        return self.rabbit.mq_connection()

    def sql_connection(self):
        """数据库连接"""
        sql_conn = Database(self)
        return sql_conn.sql_connection()

    def produce(self, url, params=None, data=None, json=None, charset=None, cookies=None, method='get', headers=None,
                callback="parse", proxies=None, allow_redirects=True, meta=None):
        """生产"""
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
        RabbitMq.publish(self.channel, js.dumps(request), self.queue_name)
        print("生产：%s" % js.dumps(request))

    def consume(self):
        """消费"""
        h = Heartbeat(self.connector, self.channel, self.queue_name)
        h.start()
        h.startheartbeat()
        self.rabbit.consume(self.channel, self.queue_name, callback=self.callback, prefetch_count=self.async_num)

    @staticmethod
    def run_forever(loop):
        """实时接收新事件"""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def start_request(self):
        """抽象生产函数"""
        pass

    def parse(self, response):
        """抽象解析函数"""
        pass

    async def deal_resp(self, ch, method, properties, body):
        """请求并回调处理响应函数"""
        try:
            if body:
                result = body.decode()
            else:
                raise
            ret = js.loads(result)
            ret['time_out'] = self.timeout
            print('消费：', ret)

            response = await self.request.quest(self.session, ret)
            if response and (response.status_code in self.allow_status_code or response.status_code == 200):
                self.__getattribute__(ret['callback'])(response)
                self.connector.add_callback_threadsafe(functools.partial(ch.basic_ack, method.delivery_tag))
            elif response:
                print("请求失败!返回状态码：%d" % response.status_code)
                # time.sleep(0.00002)
                self.produce(ret)
                self.connector.add_callback_threadsafe(functools.partial(ch.basic_ack, method.delivery_tag))
            else:
                print("请求报错!未返回消息")
                # time.sleep(0.00002)
                self.produce(ret)
                self.connector.add_callback_threadsafe(functools.partial(ch.basic_ack, method.delivery_tag))
        except Exception as e:
            print(e)
            traceback.print_exc()
            sys.exit(1)

    async def before_deal(self, ch, method, properties, body):
        await self.deal_resp(ch, method, properties, body)

    def callback(self, ch, method, properties, body):
        """rabbit_mq回调函数"""
        coroutine = self.before_deal(ch, method, properties, body)
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
        self.cursor = self.sql_connection()
        print('rabbitmq配置：', [self.mq_host, self.mq_port, self.mq_user])
        print('sql配置：', [self.sql_host, self.sql_port, self.sql_user, self.sql_db])

        # 生产消费
        if self.way and self.way == 'm':
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            if self.purge:
                RabbitMq.purge(self.channel, self.queue_name)
            else:
                print("继续生产!!!")
            self.start_request()
        elif self.way and self.way == 'w':
            self.request = Request()
            self.loop = asyncio.new_event_loop()
            self.session = self.loop.run_until_complete(self.request.new_session())

            thread = threading.Thread(target=self.run_forever, args=(self.loop,))
            thread.setDaemon(True)
            thread.start()

            self.consume()

            asyncio.run_coroutine_threadsafe(self.request.exit(self.session), self.loop)
        else:
            raise
        self.channel.close()
        self.cursor.close()


if __name__ == '__main__':
    e = Engine('w')
    e.main()
