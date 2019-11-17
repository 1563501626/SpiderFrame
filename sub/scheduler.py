# -*- coding: utf-8 -*-
import pika
import threading
import config
import time


class HeartBeat(threading.Thread):
    def __init__(self, connection):
        super(HeartBeat, self).__init__()
        self.connection = connection
        self.setDaemon(True)
        self.delay = config.heart_beat_delay

    def run(self) -> None:
        while True:
            time.sleep(self.delay)
            self.connection.process_data_events()
            print('heartbeat')


class RabbitMq:
    def __init__(self, engine):
        self.engine = engine

    def mq_connection(self):
        """初始化"""
        credentials = pika.PlainCredentials(username=self.engine.mq_user, password=self.engine.mq_pwd)
        connector = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.engine.mq_host, port=self.engine.mq_port, credentials=credentials,  heartbeat=600, blocked_connection_timeout=3000),
        )
        channel = connector.channel()
        return connector, channel

    @staticmethod
    def publish(channel, request, queue):
        """生产"""
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=request,
            properties=pika.BasicProperties(delivery_mode=2)  # 消息持久化
        )

    @staticmethod
    def callback(ch, method, properties, body):
        """回调函数"""
        print(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def consume(channel, queue, callback, prefetch_count, connection):
        """消费"""
        channel.queue_declare(queue=queue, durable=True)  # 队列持久化
        channel.basic_qos(prefetch_count=prefetch_count)
        channel.basic_consume(
            on_message_callback=callback,
            queue=queue,
            auto_ack=False,
            )
        t1 = HeartBeat(connection=connection)
        t1.start()
        channel.start_consuming()

    @staticmethod
    def purge(channel, queue_name):
        channel.queue_purge(queue_name)
        print('队列已清空!!!')


if __name__ == '__main__':
    r = RabbitMq(type('engine', (), {'mq_user': 'guest', 'mq_pwd': 'guest', 'mq_host': 'localhost', 'mq_port': 5672}))
    c = r.mq_connection()
    for i in range(10):
        r.publish(c, str(i), 'abcdef')
    print(r.consume(c, 'abcde'))