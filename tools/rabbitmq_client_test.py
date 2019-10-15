import pika


# consumer
# 连接
# credentials = pika.PlainCredentials('guest', 'guest')
connector = pika.BlockingConnection(
    pika.ConnectionParameters('127.0.0.1')
)

# 声明管道
channel = connector.channel()

# 声明队列  在不确定这个管道已声明的情况下需要在此处声明
channel.queue_declare(queue='hello')

# 回调函数
def callback(ch, method, properties, body):
    print(ch, method, properties, body)
    print('接收到消息:', body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 消费消息
channel.basic_consume(
    queue='hello',  # 监听队列名
    on_message_callback=callback, # 收到消息用callback接受处理
    auto_ack=False, # 关闭自动应答，避免消费失败而丢失数据
)

print("正在监听")
channel.start_consuming()  # 开始消费