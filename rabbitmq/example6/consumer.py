# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print("[x] Received: %r" % body)


if __name__ == "__main__":
    """
    生产者指定队列，但是不声明队列，而是直接将消息发送到该队列，消费者声明队列
    并从该队列接受消息，生产者可先运行（不报错），但是发的消息无效（被丢弃）
    只有声明队列的一方运行后，在管理界面才能看到队列
    """
    host = "127.0.0.1"
    parameters = pika.ConnectionParameters(host)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue='queue_example6')
    channel.basic_consume(callback, queue='queue_example6')

    print("[*] Waiting for message. To exit press CTRL+C")
    channel.start_consuming()
