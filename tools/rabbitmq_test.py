'https://www.zouyesheng.com/rabbitmq.html'
import pika

# producer
# 建立连接
connertor = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672)
)

# 声明管道, 在管道中发消息
channel = connertor.channel()

# 在管道中声明队列
channel.queue_declare(queue='hello')

# 声明交换机
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# 发布消息
for i in range(10):
    channel.basic_publish(
        exchange='',
        routing_key='hello',  # 队列名
        body=str(i)  # 发布内容
    )
# channel.basic_publish(
#     exchange='logs',
#     routing_key='',  # 队列名
#     body='hello world'  # 发布内容
# )
print('发布成功')
channel.close()
