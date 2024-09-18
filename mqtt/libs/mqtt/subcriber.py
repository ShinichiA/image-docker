import json
import paho.mqtt.client as paho


class MqttSubscriber:
    def __init__(self, host, port, client_id, clean_session=False):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.clean_session = clean_session
        self.client = paho.Client(client_id=self.client_id, clean_session=self.clean_session)
        self.client.on_publish = self.on_subscribe
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    @staticmethod
    def on_subscribe(client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("connected with the result code " + str(rc))

    @staticmethod
    def on_message(client, userdata, msg):
        message = msg.payload.decode("utf-8")
        res = json.loads(message)
        if isinstance(res, dict):
            print(res, 'dict')
            return
        print(res)

    def connect(self, topic, qos, keepalive=60, bind_address="", bind_port=0, clean_start="", properties=None):
        # self.client.username_pw_set("iot_pub", "zFCL7IvuW0e!aF3s3d5rb")
        # self.client.tls_set("./mqtt_certificate/ca.crt", "./mqtt_certificate/mqtt.crt", "./mqtt_certificate/mqtt.key")
        # self.client.tls_insecure_set(True)
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic=topic, qos=qos)

    def start_loop(self):
        self.client.loop_forever()

    def disconnect(self):
        self.client.loop_stop()
