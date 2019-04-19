# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print("[x] Received: %r" % body)


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
    channel.queue_declare(queue='queue_example1')
    channel.queue_bind(queue='queue_example1', exchange='exchange_example1', routing_key='')

    channel.basic_consume(callback, queue='queue_example1')

    print("[*] Waiting for message. To exit press CTRL+C")
    channel.start_consuming()
