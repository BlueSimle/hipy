# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print("[x] Received: %r" % body)


if __name__ == "__main__":
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(exchange='exchange_example9', exchange_type='topic')
    channel.exchange_bind()

    # 随机创建队列，exclusive=True 表示建立临时队列，当 consumer 关闭后，该队列就会自动删除
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    # 将队列与 exchange 绑定
    channel.queue_bind(exchange='exchange_example9', queue=queue_name, routing_key="key_example9.#")

    channel.basic_consume(callback, queue=queue_name)

    print("[*] Waiting for message. To exit press CTRL+C")
    channel.start_consuming()
