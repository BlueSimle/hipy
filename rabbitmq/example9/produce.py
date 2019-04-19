# -*- coding: utf-8 -*-

import pika
import random

if __name__ == "__main__":
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(exchange='exchange_example9', exchange_type='topic')

    body = "hello world: {number}".format(number=random.randint(1, 100))

    channel.basic_publish(exchange='exchange_example9', routing_key='key_example9.cacd', body=body)

    print("[x] Sent %s" % body)

    connection.close()
