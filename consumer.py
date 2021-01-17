#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: huangshan
# datetime: 2021-01-17 12:41
# software: PyCharm

import pika, json

from main import Product, db

amqpUrl = "amqps://favhlvqn:LM9kccEJ9RNfPUuolNurqHzPXClFkP-m@orangutan.rmq.cloudamqp.com/favhlvqn"

params = pika.URLParameters(amqpUrl)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='integral')


def callback(ch, method, properties, body):
    print('Received in integral')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created')
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product deleted')


channel.basic_consume(queue='integral', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
