# -*- coding: utf-8 -*-
import config
from sub.scheduler import RabbitMq
from sub.item_pipline import Database
from sub.spiders import Request, Response

import json as js
import asyncio
import threading


class Engine:
    def __init__(self, way):
        self.mq_host = None
        self.mq_port = None
        self.mq_user = None
        self.mq_pwd = None
        self.sql_host = None
        self.sql_port = None
        self.sql_user = None
        self.sql_pwd = None
        self.sql_db = None
        self.async_num = 2
        # self.way = None
        self.way = way
        self.queue_name = None
        self.parse_callback = None

        self.channel = None
        self.cursor = None

        self.purge = True
        self.loop = None
        self.request = None
        self.session = None
        self.allow_status_code = [200]

    def mq_connection(self):
        mq_conn = RabbitMq(self)
        return mq_conn.mq_connection()

    def sql_connection(self):
        sql_conn = Database(self)
        return sql_conn.sql_connection()

    def produce(self, url, method="get", params=None, data=None, json=None, callback='parse', session=None):
        request = {
            'url': url,
            'method': method,
            'params': params,
            'data': data,
            'json': json,
            'callback': callback,
            'session': session,
        }
        RabbitMq.publish(self.channel, js.dumps(request), self.queue_name)
        print("生产：%s" % js.dumps(request))

    def consume(self):
        RabbitMq.consume(self.channel, self.queue_name, callback=self.callback, prefetch_count=self.async_num)


    @staticmethod
    def run_forever(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def start_request(self):
        for i in ['http://www.baidu.com', 'http://www.baidu.com/s?wd=hello', 'http://www.baidu.com/s?wd=xixi', 'http://www.baidu.com/s?wd=hello', 'http://www.baidu.com/s?wd=xixi', 'http://www.baidu.com/s?wd=hello', 'http://www.baidu.com/s?wd=xixi']:
            self.produce(i)

    def parse(self, response):
        pass

    def callback(self, ch, method, properties, body):
        """rabbit_mq回调函数"""
        if body:
            ret = body.decode()
        else:
            raise

        print('消费：', ret)
        ret = js.loads(ret)
        self.parse_callback = ret['callback']
        coroutine = self.request.quest(self.session, method=ret['method'], url=ret['url'])
        fs = asyncio.run_coroutine_threadsafe(coroutine, self.loop)
        fs.add_done_callback(self.func)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def func(self, future):
        ret = future.result()
        body = ret[0]
        res = ret[1]
        if res.status_code in self.allow_status_code:
            response = Response(body)
            if hasattr(self, self.parse_callback):
                self.__getattribute__(self.parse_callback)(response)
            else:
                raise

    def main(self):
        """main"""
        # 配置文件初始化
        serious = ['mq_host', 'mq_port', 'mq_user', 'mq_pwd', 'sql_host', 'sql_port', 'sql_user', 'sql_pwd', 'sql_db']
        for i in serious:
            if hasattr(self, i) and getattr(self, i) is None:
                attr = getattr(config, i)
                setattr(self, i, attr if attr else None)
        self.queue_name = __name__

        # 创建连接
        self.channel = self.mq_connection()
        self.cursor = self.sql_connection()
        print('连接')
        # 生产消费
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
            self.consume()

            asyncio.run_coroutine_threadsafe(self.request.exit(self.session), self.loop)  # -------------------

        self.channel.close()
        self.cursor.close()


if __name__ == '__main__':
    e = Engine('w')
    e.main()