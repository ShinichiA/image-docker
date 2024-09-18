import pika

# using CloudAMQP (https://www.cloudamqp.com/)
CLOUDAMQP_URL = 'amqp://anhbt:maimai95@localhost:5672/camera?connection_attempts=3&heartbeat=60'

# establish a connection with RabbitMQ server.
params = pika.URLParameters(CLOUDAMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

properties = pika.BasicProperties(content_type='application/json', delivery_mode=2)
no = 0
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=f"{no}")

no += 1
print(" Sent message")
connection.close()
