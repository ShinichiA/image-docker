import json
import paho.mqtt.client as paho


class MqttPublisher:
    def __init__(self, host, port, client_id, user=None, password=None, crt=False, clean_session=False):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.clean_session = clean_session
        self.client = paho.Client(client_id=self.client_id, clean_session=self.clean_session)
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect
        self.user = user
        self.password = password
        self.crt = crt

    @staticmethod
    def on_publish(client, userdata, mid):
        print("mid: " + str(mid))

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("connected with the result code " + str(rc))

    def connect(self, keepalive=60, bind_address="", bind_port=0, clean_start=None, properties=None, lwt_topic=None):
        if lwt_topic:
            self.will_set(lwt_topic)
        self.client.username_pw_set("iot_pub", "zFCL7IvuW0e!aF3s3d5rb")
        if self.crt:
            self.client.tls_set("./libs/mqtt/mqtt_certificate/ca.crt", "./libs/mqtt/mqtt_certificate/mqtt.crt", "./libs/mqtt/mqtt_certificate/mqtt.key")
            self.client.tls_insecure_set(True)
        self.client.connect(host=self.host, port=self.port)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()

    def will_set(self, lwt_topic, qos=1, retain=True, message_will_set='{"status": "OFFLINE"}'):
        self.client.will_set(lwt_topic, payload=json.dumps(message_will_set), qos=qos, retain=retain)

    def publish_message(self, topic, message, qos=1, retain=False):
        return self.client.publish(topic, json.dumps(message), qos=qos, retain=retain)
