# -*- coding: utf-8 -*-
import pika
import requests
import json
import config
import logging

logger = logging.getLogger(__name__)


class RabbitMq:
    def __init__(self, engine):
        self.engine = engine

    def mq_connection(self):
        """初始化"""
        credentials = pika.PlainCredentials(username=self.engine.mq_user, password=self.engine.mq_pwd)
        connector = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.engine.mq_host, port=self.engine.mq_port, credentials=credentials,
                                      heartbeat=0),
        )
        channel = connector.channel()
        return connector, channel

    @staticmethod
    def mq_connection_from_config():
        credentials = pika.PlainCredentials(username=config.mq_user, password=config.mq_pwd)
        connector = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.mq_host, port=config.mq_port, credentials=credentials,
                                      heartbeat=0),
        )
        channel = connector.channel()
        return connector, channel

    @staticmethod
    def publish(channel, request, queue):
        """发布"""
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=request,
            properties=pika.BasicProperties(delivery_mode=2)  # 消息持久化
        )

    def sure_conn(self, queue, connector, channel):
        if not channel:
            return connector, channel
        try:
            channel.queue_declare(queue=queue, durable=True)
        except Exception as e:
            connector, channel = self.mq_connection()
            channel.queue_declare(queue=queue, durable=True)
            print('pika超时，已重连！')
        return connector, channel

    @staticmethod
    def callback(ch, method, properties, body):
        """回调函数"""
        logger.info(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def consume(channel, queue, callback, prefetch_count):
        """消费"""
        channel.queue_declare(queue=queue, durable=True)  # 队列持久化
        channel.basic_qos(prefetch_count=prefetch_count)
        channel.basic_consume(
            on_message_callback=callback,
            queue=queue,
            auto_ack=False)
        channel.start_consuming()

    @staticmethod
    def is_empty(queue_name):
        rabbitmq_host = config.mq_host
        rabbitmq_user = config.mq_user
        rabbitmq_pwd = config.mq_pwd
        rabbitmq_port = 15672
        res = requests.get(
            url='http://{}:{}/api/queues/{}/{}'.format(rabbitmq_host, rabbitmq_port, "%2F", queue_name),
            auth=(rabbitmq_user, rabbitmq_pwd)
        )
        res = json.loads(res.content.decode())
        print(res)
        if "messages" not in res.keys():
            return 0
        return int(res["messages"])

    @staticmethod
    def del_queue(channel, queue_name, if_unused=False, if_empty=True):
        channel.queue_delete(queue=queue_name, if_unused=if_unused, if_empty=if_empty)

    @staticmethod
    def purge(channel, queue_name):
        channel.queue_purge(queue_name)
        logger.info('队列已清空!!!')


if __name__ == '__main__':
    pass
