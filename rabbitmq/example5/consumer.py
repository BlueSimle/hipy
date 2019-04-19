# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print("[x] Received: %r" % body)


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
    channel.basic_consume(callback, queue='queue_example5')

    print("[*] Waiting for message. To exit press CTRL+C")
    channel.start_consuming()
