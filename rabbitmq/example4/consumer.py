# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print("[x] Received: %r" % body)


if __name__ == "__main__":
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue='queue_example4')
    channel.basic_consume(callback, queue='queue_example4')

    print("[*] Waiting for message. To exit press CTRL+C")
    channel.start_consuming()
