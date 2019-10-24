# -*- coding: utf-8 -*-
import config
from sub.scheduler import RabbitMq
from sub.item_pipline import Database

import json as js


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
        self.async_num = 1
        # self.way = None
        self.way = way
        self.queue_name = None

        self.channel = None
        self.cursor = None

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
        RabbitMq.consume(self.channel, self.queue_name, callback='callback', prefetch_count=self.async_num)

    def start_request(self):
        for i in range(10):
            url = 'http://test.html/' + str(i)
            self.produce(url)

    def parse(self, response):
        pass

    def callback(self, ch, method, properties, body):
        """回调函数"""
        if body:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return body.decode()

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

        # 生产消费
        if self.way and self.way == 'm':
            self.start_request()
        elif self.way and self.way == 'w':
            body = js.loads(self.consume())

        self.channel.close()
        self.cursor.close()


if __name__ == '__main__':
    e = Engine('m')
    e.main()