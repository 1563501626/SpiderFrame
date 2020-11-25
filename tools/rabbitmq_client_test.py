import time

from sub.queues import RabbitMq
import json
connector, channel = RabbitMq.mq_connection_from_config()

old = []
young = []
kid = []
while True:
    r = RabbitMq.is_empty()
    for i in r:
        try:
            messages = i['messages']
        except Exception as e:
            print("*****************", e, "******************")
            continue
        if messages == 0:
            name = i['name']
            if name in kid:
                kid.remove(name)
                young.append(name)
            elif name in young:
                young.remove(name)
                old.append(name)
            elif name in old:
                RabbitMq.del_queue(channel, name)
                old.remove(name)
                time.sleep(1)
                print("kill %s" % name)
            else:
                kid.append(name)
    print("waiting ~~~")
    time.sleep(30)
