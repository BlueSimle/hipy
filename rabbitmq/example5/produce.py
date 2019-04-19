# -*- coding: utf-8 -*-

import pika
import random

if __name__ == "__main__":
    """
    生产者声明队列并将消息发送到该队列，消费者也声明该队列，并从该队列消费消息，
    但是：生产者和消费者声明队列时指定的参数要一直，否则会报错
    """
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue='queue_example5')
    body = "hello world: {number}".format(number=random.randint(1, 100))
    channel.basic_publish(exchange='', routing_key='queue_example5', body=body)
    print("[x] Sent %s" % body)

    connection.close()
