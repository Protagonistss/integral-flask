#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: huangshan
# datetime: 2021-01-17 12:41
# software: PyCharm

import pika

amqpUrl = "amqps://favhlvqn:LM9kccEJ9RNfPUuolNurqHzPXClFkP-m@orangutan.rmq.cloudamqp.com/favhlvqn"

params = pika.URLParameters(amqpUrl)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='integral')


def callback(ch, method, properties, body):
    print('Received in integral')
    print(body)


channel.basic_consume(queue='integral', on_message_callback=callback)

print('Started Consuming')

channel.start_consuming()

channel.close()
