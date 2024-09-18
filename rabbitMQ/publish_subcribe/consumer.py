# import pika
#
# CLOUDAMQP_URL = 'amqp://anhbt:maimai95@localhost:5672/camera?connection_attempts=3&heartbeat=600'
#
# # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
# params = pika.URLParameters(CLOUDAMQP_URL)
# connection = pika.BlockingConnection(params)
# channel = connection.channel()  # start a channel
# channel.queue_declare(queue='camera')  # Declare a queue
#
# channel.basic_qos(prefetch_count=1)
#
#
# def callback(ch, method, properties, body):
#     print(" [x] Received " + str(body))
#     channel.basic_ack(delivery_tag=method.delivery_tag, multiple=True)
#
#
# channel.basic_consume('camera',
#                       callback,
#                       auto_ack=False,
#                       exclusive=True,
#                       consumer_tag='camera')
#
# print(' [*] Waiting for messages:')
# channel.start_consuming()
# connection.close()

import pika

CLOUDAMQP_URL = 'amqp://anhbt:maimai95@localhost:5672/camera?connection_attempts=3&heartbeat=600'
params = pika.URLParameters(CLOUDAMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
