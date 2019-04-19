# -*- coding: utf-8 -*-

import pika
import random

if __name__ == "__main__":
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    body = "hello world: {number}".format(number=random.randint(1, 100))
    channel.basic_publish(exchange='', routing_key='queue_example4', body=body)

    print("[x] Sent %s" % body)

    connection.close()
