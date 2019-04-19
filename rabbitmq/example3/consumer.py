# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print("[x] Received: %r" % body)


if __name__ == "__main__":
    """
    生产者声明队列（指定队列名称），消费者不指定队列，而是直接消费生产者指定的队列，
    但是此时，声明队列的一方要先运行，否则消费者连不上队列，会保持
    """
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.basic_consume(callback, queue='queue_example3')

    print("[*] Waiting for message. To exit press CTRL+C")
    channel.start_consuming()
