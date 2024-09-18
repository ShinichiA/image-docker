import base64
import json

import pika

# CLOUDAMQP_URL = 'amqp://iot_rabbitmq:Ghtk@iot@2020@10.110.76.246:5672/smsc_manager?connection_attempts=3&heartbeat=600'
CLOUDAMQP_URL = 'amqp://anhbt:maimai95@localhost:5672/camera?connection_attempts=3&heartbeat=60'

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
params = pika.URLParameters(CLOUDAMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel
queue_ok = channel.queue_declare(queue="camera.video_download_request.queue",
                                 durable=True,
                                 exclusive=False,
                                 auto_delete=False,
                                 passive=False)

channel.basic_qos(prefetch_count=1)


def callback(ch, method, properties, body):
    buffer = base64.b64decode(body)
    mac = properties.headers.get('mac')
    with open('./a.jpg', "wb") as f:
        f.write(buffer)
    channel.basic_ack(delivery_tag=method.delivery_tag, multiple=True)


channel.basic_consume(queue='camera.video_download_request.queue',
                      on_message_callback=callback,
                      auto_ack=False,
                      exclusive=False,
                      consumer_tag='camera')

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
