# -*- coding: utf-8 -*-

import pika
import random

if __name__ == "__main__":
    """
    生产者声明队列（指定队列名称），消费者不指定队列，而是直接消费生产者指定的队列，
    但是此时，声明队列的一方要先运行，否则消费者连不上队列，会报错
    """
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue='queue_example3')

    body = "hello world: {number}".format(number=random.randint(1, 100))

    # delivery_mode=2 声明持久化存储
    channel.basic_publish(exchange='', routing_key='queue_example3', body=body)

    print("[x] Sent %s" % body)

    connection.close()
