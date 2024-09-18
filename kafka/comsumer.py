import time
from kafka import KafkaConsumer, TopicPartition
from json import loads

consumer = KafkaConsumer(
    bootstrap_servers=['localhost:29092'],
    auto_offset_reset='latest',
    auto_commit_interval_ms=1000,
    enable_auto_commit=False,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

consumer.assign([TopicPartition("camera", 1), TopicPartition("camera-2", 0)])


for message in consumer:
    message = message.value
    print('message: {}'.format(message))
    consumer.commit()
