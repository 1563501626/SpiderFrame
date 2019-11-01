# -*- coding: utf-8 -*-
import pika


class RabbitMq:
    def __init__(self, engine):
        self.engine = engine

    def mq_connection(self):
        """初始化"""
        credentials = pika.PlainCredentials(username=self.engine.mq_user, password=self.engine.mq_pwd)
        connector = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.engine.mq_host, port=self.engine.mq_port, credentials=credentials)
        )
        channel = connector.channel()
        return channel

    @staticmethod
    def publish(channel, request, queue):
        """生产"""
        channel.queue_declare(queue=queue, durable=True)  # 队列持久化
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
    def consume(channel, queue, callback, prefetch_count):
        """消费"""
        channel.queue_declare(queue=queue, durable=True)  # 队列持久化
        channel.basic_qos(prefetch_count=prefetch_count)
        channel.basic_consume(
            queue=queue,
            on_message_callback=callback,
            auto_ack=False)
        channel.start_consuming()

    def del_queue(self, name, if_unused=False, if_empty=False):
        self.channel.queue_delete(queue=name, if_unused=if_unused, if_empty=if_empty)

    @staticmethod
    def purge(channel, queue_name):
        channel.queue_purge(queue_name)
        print('队列已清空!!!')


if __name__ == '__main__':
    r = RabbitMq(type('engine', (), {'mq_user': 'guest', 'mq_pwd': 'guest', 'mq_host': 'localhost', 'mq_port': 5672}))
    c = r.mq_connection()
    for i in range(10):
        r.publish(c, str(i), 'abcdef')
    print(r.consume(c, 'abcdef', r.callback, 2))