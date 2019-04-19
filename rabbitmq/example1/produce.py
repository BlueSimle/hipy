# -*- coding: utf-8 -*-

import pika
import random

if __name__ == "__main__":
    """
    1. 生产者指定了 exchange 和 routing key, 但是不指定 queue，也不将 queue 绑定到 exchange
    2. 队列声明和绑定到 exchange 的工作由消费者完成
    """
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(exchange='exchange_example1')
    body = "hello world: {number}".format(number=random.randint(1, 100))
    channel.basic_publish(exchange='exchange_example1', routing_key='', body=body)

    print("[x] Sent %s" % body)

    connection.close()
