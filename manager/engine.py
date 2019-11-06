# -*- coding: utf-8 -*-
import config
from sub.scheduler import RabbitMq
from sub.item_pipline import Database
from sub.spiders import Request

import json as js
import asyncio
import threading
import functools


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

        self.connector = None
        self.channel = None
        self.cur_queue = None
        self.if_unused = False
        self.if_empty = False
        self.cursor = None

        self.purge = True
        self.loop = None
        self.request = None
        self.session = None
        self.allow_status_code = [200]
        self.retry = 3

    def mq_connection(self):
        mq_conn = RabbitMq(self)
        return mq_conn.mq_connection()

    def sql_connection(self):
        sql_conn = Database(self)
        return sql_conn.sql_connection()

    def produce(self, url, params=None, data=None, json=None, charset=None, cookies=None, method='get', headers=None,
                callback="parse", proxies=None, time_out=None, allow_redirects=True, meta=None):
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
            'time_out': time_out,
            'allow_redirects': allow_redirects,
            'meta': meta
        }
        RabbitMq.publish(self.channel, js.dumps(request), self.queue_name)
        print("生产：%s" % js.dumps(request))

    def consume(self):
        while True:

            RabbitMq.consume(self.channel, self.queue_name, callback=self.callback, prefetch_count=self.async_num)
            break

    @staticmethod
    def run_forever(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def start_request(self):
        pass

    def parse(self, response):
        pass

    async def deal_resp(self, ch, method, properties, body):
        if body:
            result = body.decode()
        else:
            raise

        ret = js.loads(result)
        print('消费：', ret)

        response = await self.request.quest(self.session, ret)

        if response.status_code in self.allow_status_code:
            self.__getattribute__(ret['callback'])(response)
            self.connector.add_callback_threadsafe(functools.partial(ch.basic_ack, method.delivery_tag))
        else:
            print("请求报错!返回状态码：%d" % response.status_code, end=' ')
            self.produce(ret['url'])  # TODO// ++++++++++++++++++++++++++++++
            self.connector.add_callback_threadsafe(functools.partial(ch.basic_ack, method.delivery_tag))

    def callback(self, ch, method, properties, body):
        """rabbit_mq回调函数"""
        coroutine = self.deal_resp(ch, method, properties, body)
        asyncio.run_coroutine_threadsafe(coroutine, self.loop)

    def del_queue(self):
        while True:
            count = self.cur_queue.method.message_count
            print(count)
            if count == 0:
                self.channel.queue_delete(queue=self.queue_name, if_unused=self.if_unused, if_empty=self.if_empty)

    def main(self):
        """main"""
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
        self.cur_queue = self.channel.queue_declare(queue=self.queue_name, durable=True)
        if self.way and self.way == 'm':

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

            delete_thread = threading.Thread(target=self.del_queue)
            delete_thread.start()
            self.consume()
            delete_thread.join(30)

            asyncio.run_coroutine_threadsafe(self.request.exit(self.session), self.loop)  # TODO// ++++++++++++++++++++++++++++++
        else:
            raise
        self.channel.close()
        self.cursor.close()


if __name__ == '__main__':
    e = Engine('w')
    e.main()
