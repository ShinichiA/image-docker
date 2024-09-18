import base64
import json
from data import *

import pika

# using CloudAMQP (https://www.cloudamqp.com/)
CLOUDAMQP_URL = 'amqp://anhbt:maimai95@localhost:5672/camera?connection_attempts=3&heartbeat=60'
# CLOUDAMQP_URL = 'amqp://admin:m6qEYVQFe9nWZypPDFpKSkAJ@10.110.69.90:5672/camera_manager_testing?connection_attempts=3&heartbeat=60'

# establish a connection with RabbitMQ server.
params = pika.URLParameters(CLOUDAMQP_URL)
connection = pika.BlockingConnection(params)

# channel 1
channel = connection.channel()

exchange_ok = channel.exchange_declare(exchange='camera.video_download_request.ex', durable=True,
                                       exchange_type='direct')
queue_ok = channel.queue_declare(queue='camera.video_download_request.queue',
                                 durable=True,
                                 exclusive=False,
                                 auto_delete=False,
                                 passive=False, )

bind_ok = channel.queue_bind(queue='camera.video_download_request.queue',
                             exchange='camera.video_download_request.ex',
                             routing_key='camera.video_download_request.route')

# publish message
properties = pika.BasicProperties(content_type='application/json', delivery_mode=2, headers={'mac': "1234"})
f = open('./1.jpg', 'rb')
# publish message can co exchange va routing_key
# routing_key = queue name

channel.basic_publish(exchange='camera.video_download_request.ex',
                      routing_key='camera.video_download_request.route',
                      body=json.dumps({'picture' : f.read().encode('base64')}),
                      properties=properties)

connection.close()
