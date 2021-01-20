#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: huangshan
# datetime: 2021-01-16 22:26
# software: PyCharm

import pika, json, os

amqpUrl = os.getenv('AMQPURL')
paramas = pika.URLParameters(amqpUrl)
connection = pika.BlockingConnection(paramas)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
