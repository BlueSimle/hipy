# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print("[x] Received: %r" % body)


if __name__ == "__main__":
    """
    1. 生产者指定 exchange 和 routing key, 声明队列并将队列绑定到 exchange, 
    2. 消费者只需从生成者绑定的队列消费即可
    """
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.basic_consume(callback, queue='queue_example2')

    print("[*] Waiting for message. To exit press CTRL+C")
    channel.start_consuming()
