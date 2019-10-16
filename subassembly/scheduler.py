# -*- coding: utf-8 -*-
import pika


def connect_mq(host, port, user, pwd):
    """初始化"""
    credentials = pika.PlainCredentials(username=user, password=pwd)
    connector = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    )
    channel = connector.channel()
    return channel


def publish(channel, body, queue):
    """生产"""
    channel.queue_declare(queue=queue)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=body
    )


def callback(ch, method, properties, body):
    """回调函数"""
    pass


def consume(channel, queue):
    """消费"""
    channel.queue_declare(queue=queue)
    channel.basic_consume(
        queue=queue,
        on_message_callback=callback,
        auto_ack=False,
    )


if __name__ == '__main__':
    pass