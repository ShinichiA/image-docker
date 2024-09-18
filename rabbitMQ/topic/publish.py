import pika

# using CloudAMQP (https://www.cloudamqp.com/)
# retry connect 3 times. 60/2s send heartbeat check TCP alive
CLOUDAMQP_URL = 'amqp://anhbt:maimai95@localhost:5672/camera?connection_attempts=3&heartbeat=60'

# establish a connection with RabbitMQ server.
params = pika.URLParameters(CLOUDAMQP_URL)
connection = pika.BlockingConnection(params)

# channel 1
channel = connection.channel()

exchange_ok = channel.exchange_declare(exchange='camera.topic', durable=True, exchange_type='topic')
queue_ok = channel.queue_declare(queue='camera_topic',
                                 durable=True,
                                 exclusive=False,
                                 auto_delete=False,
                                 passive=False,
                                 arguments={'x-max-priority': 10})

bind_ok = channel.queue_bind(queue='camera_topic',
                             exchange='camera.topic',
                             routing_key='*.info')


# channel 2
channel2 = connection.channel()
channel2.exchange_declare(exchange='camera.topic', durable=True, exchange_type='topic')
channel2.queue_declare(queue='camera_topic_1',
                       durable=True,
                       exclusive=False,
                       auto_delete=False,
                       passive=False,
                       arguments={'x-max-priority': 10})

# binding info
channel2.queue_bind(queue='camera_topic_1',
                    exchange='camera.topic',
                    routing_key='lazy.*')

# publish message
properties = pika.BasicProperties(content_type='application/json', delivery_mode=2)

# publish message can co xchange va routing_key
# routing_key = queue name
channel.basic_publish(exchange='camera.topic',
                      routing_key='lazy.info',
                      body=f"{1}",
                      properties=properties)

print(" Sent message")
connection.close()
