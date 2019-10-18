# -*- coding: utf-8 -*-
import pika


class RabbitMq:
    def __init__(self, engine):
        self.engine = engine

    def mq_connection(self):
        """初始化"""
        credentials = pika.PlainCredentials(username=self.engine.user, password=self.engine.pwd)
        connector = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.engine.host, port=self.engine.port, credentials=credentials)
        )
        channel = connector.channel()
        return channel

    def publish(self, channel, request, queue):
        """生产"""
        channel.queue_declare(queue=queue, durable=True)  # 队列持久化
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=request,
            properties=pika.BasicProperties(delivery_mode=2)  # 消息持久化
        )

    def callback(self, ch, method, properties, body):
        """回调函数"""
        print(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self, channel, queue):
        """消费"""
        channel.queue_declare(queue=queue, durable=True)  # 队列持久化
        channel.basic_consume(
            queue=queue,
            on_message_callback=self.callback,
            auto_ack=False)


if __name__ == '__main__':
    r = RabbitMq(type('engine', (), {'user': 'guest', 'pwd': 'guest', 'host': 'localhost', 'port': 5672}))
    c = r.mq_connection()
    r.publish(c, type('r', (), {'data': 1}), 'abcdef')
    r.consume(c, 'abcdef')