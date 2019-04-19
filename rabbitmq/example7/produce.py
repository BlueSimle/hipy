# -*- coding: utf-8 -*-

import pika
import random

if __name__ == "__main__":
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(exchange='exchange_example7', exchange_type='fanout')

    body = "hello world: {number}".format(number=random.randint(1, 100))

    # fanout 模式下不需要配置 routing key, 配置了也不会生效
    channel.basic_publish(exchange='exchange_example7', routing_key='', body=body)

    print("[x] Sent %s" % body)

    connection.close()
