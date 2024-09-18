from datetime import datetime

import pika

# using CloudAMQP (https://www.cloudamqp.com/)
CLOUDAMQP_URL = 'amqp://anhbt:maimai95@localhost:5672/camera?connection_attempts=3&heartbeat=60'

# establish a connection with RabbitMQ server.
params = pika.URLParameters(CLOUDAMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

queue_ok = channel.queue_declare(queue='camera_worker',
                                 durable=True,
                                 exclusive=False,
                                 auto_delete=False,
                                 passive=False,
                                 arguments={'x-max-priority': 10})

properties = pika.BasicProperties(content_type='application/json', delivery_mode=2)
no = 0
# routing_key = queue name
channel.basic_publish(exchange='',
                      routing_key='camera_worker',
                      body=f"{no}",
                      properties=properties)
print(datetime.now())
print(" Sent message")
connection.close()
