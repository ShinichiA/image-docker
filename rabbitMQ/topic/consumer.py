import pika

CLOUDAMQP_URL = 'amqp://anhbt:maimai95@localhost:5672/camera?connection_attempts=3&heartbeat=600'

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
params = pika.URLParameters(CLOUDAMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel
queue_ok = channel.queue_declare(queue='camera',
                                 durable=True,
                                 exclusive=False,
                                 auto_delete=False,
                                 passive=False,
                                 arguments={'x-max-priority': 10})

channel.basic_qos(prefetch_count=1)


def callback(ch, method, properties, body):
    print(" [x] Received " + str(body))
    channel.basic_ack(delivery_tag=method.delivery_tag, multiple=True)


channel.basic_consume(queue='camera',
                      on_message_callback=callback,
                      auto_ack=False,
                      exclusive=False,
                      consumer_tag='camera')

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
