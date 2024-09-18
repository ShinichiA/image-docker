from threading import Thread
from libs.mqtt import MqttSubscriber


class MqttThread(Thread):
    def __init__(self, host, port, topic, client_id, clean_session=False):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.topic = topic
        self.client_id = client_id
        self.clean_session = clean_session

    def run(self) -> None:
        mqtt_subscribe = MqttSubscriber(host=self.host, port=self.port, client_id=self.client_id,
                                        clean_session=self.clean_session)
        mqtt_subscribe.connect(topic=self.topic, qos=2)
        mqtt_subscribe.start_loop()
