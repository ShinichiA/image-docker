import time
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:29092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

for e in range(1000):
    data = {'number': e}
    # producer.send('camera', value=data, partition=1)
    producer.send('camera', value=data, partition=1)
    producer.send('camera-2', value=data, partition=0)
    time.sleep(0.1)
