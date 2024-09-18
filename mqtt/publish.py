import time
from libs.mqtt import MqttPublisher

topic = "encyclopedia/temperature"
mqtt_publisher = MqttPublisher(host='localhost', port=1883, client_id='world_pub', clean_session=False)
mqtt_publisher.connect(lwt_topic=topic)

while True:
    (rc, mid) = mqtt_publisher.publish_message(topic, {'1': '2'}, qos=2, retain=True)
    time.sleep(2)
